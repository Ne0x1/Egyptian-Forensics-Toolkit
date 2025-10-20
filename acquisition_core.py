import os
import sys
import time
import hashlib
import subprocess
from datetime import datetime

# --- استيراد الأدوات المساعدة ---
from utils import log_message, BAD_SECTOR_LOG

# === GLOBAL CONFIGURATION === #
BUFFER_SIZE = 1024 * 1024  # 1MB buffer for I/O

# === HELPER FUNCTIONS (Acquisition Specific) === #

def get_source_size(source_path):
    """Gets the size of the source, whether it's a file or a block device."""
    try:
        if os.path.isfile(source_path):
            return os.path.getsize(source_path)
        elif sys.platform.startswith('linux'):
            # This is Linux-specific. For other OSes, a different command would be needed.
            return int(subprocess.check_output(["blockdev", "--getsize64", source_path]))
        else:
            # Fallback for non-Linux block devices (might not always work)
            fd = os.open(source_path, os.O_RDONLY)
            size = os.lseek(fd, 0, os.SEEK_END)
            os.close(fd)
            return size
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(f"[!] Critical: Could not determine size of source '{source_path}'. Error: {e}")
        return 0

def set_write_block(device, state):
    """Attempts to enable/disable software write-blocking on Linux. DANGEROUS."""
    if not sys.platform.startswith('linux') or not os.path.exists(device) or os.path.isfile(device):
        return # Only for Linux block devices

    command = "ro" if state else "rw"
    try:
        print(f"[*] Attempting to set device {device} to {command}...")
        subprocess.run(["blockdev", f"--set{command}", device], check=True)
        print(f"[+] Successfully set {device} to read-only.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[!] WARNING: Failed to set software write-block on {device}. Error: {e}")
        print("[!] PROCEED WITH EXTREME CAUTION. A HARDWARE WRITE-BLOCKER IS STRONGLY RECOMMENDED.")
        input("    Press Enter to continue at your own risk, or Ctrl+C to abort...")
        return False


# === CORE ACQUISITION LOGIC === #

def acquire_image(args, log_file):
    """
    Main acquisition function. Reads the source once and performs hashing and writing
    simultaneously. Also handles bad sectors.
    """
    log_message(log_file, "Acquisition process started.")
    
    source_path = args.source
    output_raw_path = os.path.join(args.output_dir, "image.dd")
    
    # Attempt to apply software write-block
    set_write_block(source_path, True)
    
    total_bytes = get_source_size(source_path)
    if total_bytes == 0:
        log_message(log_file, "Error: Source size is 0 or could not be determined. Aborting.")
        return None, {}

    md5_hasher = hashlib.md5()
    sha256_hasher = hashlib.sha256()
    
    bytes_read = 0
    bad_sectors = 0
    start_time = time.time()

    log_message(log_file, f"Source: {source_path} ({total_bytes} bytes)")
    log_message(log_file, f"Destination (RAW): {output_raw_path}")
    
    try:
        with open(source_path, 'rb') as src, open(output_raw_path, 'wb') as dst:
            while True:
                chunk = b''
                try:
                    # نقرأ حتى لو أقل من البافر في نهاية الملف
                    bytes_to_read = min(BUFFER_SIZE, total_bytes - bytes_read)
                    if bytes_to_read <= 0:
                        break # وصلنا للنهاية
                        
                    chunk = src.read(bytes_to_read)
                    if not chunk:
                        break # End of file
                    
                    # 1. Update hashes with the good chunk
                    md5_hasher.update(chunk)
                    sha256_hasher.update(chunk)
                    
                    # 2. Write the good chunk to the destination
                    dst.write(chunk)
                    
                    bytes_read += len(chunk)

                except IOError as e:
                    # --- BAD SECTOR HANDLING --- #
                    bad_sectors += 1
                    sector_pos = src.tell()
                    log_message(log_file, f"[!] Read error (bad sector) at offset: {sector_pos}. Error: {e}")
                    log_message(BAD_SECTOR_LOG, f"Read error (bad sector) at offset: {sector_pos}. Error: {e}")
                    
                    # نكتب أصفار بحجم البافر أو ما تبقى من الملف
                    bytes_to_write = min(BUFFER_SIZE, total_bytes - bytes_read)
                    if bytes_to_write <= 0:
                        break

                    # Skip the bad block in the source
                    try:
                        src.seek(bytes_to_write, 1) # 1 = os.SEEK_CUR
                    except Exception as seek_e:
                        log_message(log_file, f"[!] Critical seek error: {seek_e}. Aborting.")
                        break

                    # Write a block of zeros to the destination to maintain size
                    dst.write(b'\x00' * bytes_to_write)
                    
                    bytes_read += bytes_to_write
                
                # --- Progress Reporting --- #
                percent = (bytes_read / total_bytes) * 100
                elapsed = time.time() - start_time
                mb_per_sec = (bytes_read / (1024*1024)) / elapsed if elapsed > 0 else 0
                sys.stdout.write(
                    f"\r[+] Progress: {percent:.2f}% | {mb_per_sec:.2f} MB/s | Bad Sectors: {bad_sectors}..."
                )
                sys.stdout.flush()

    except Exception as e:
        log_message(log_file, f"A critical error occurred during imaging: {e}")
        return None, {}
    finally:
        # Revert write-block state
        set_write_block(source_path, False)

    hashes = {
        "md5": md5_hasher.hexdigest(),
        "sha256": sha256_hasher.hexdigest(),
    }
    
    end_time = time.time()
    # طباعة سطر جديد بعد شريط التقدم
    sys.stdout.write('\n')
    sys.stdout.flush()
    
    log_message(log_file, f"RAW imaging complete. Time: {end_time - start_time:.2f}s")
    log_message(log_file, f"MD5 Hash: {hashes['md5']}")
    log_message(log_file, f"SHA256 Hash: {hashes['sha256']}")
    log_message(log_file, f"Total Bad Sectors: {bad_sectors}")
    
    return output_raw_path, hashes