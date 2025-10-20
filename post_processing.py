import os
import getpass
import subprocess
import shutil
from datetime import datetime

# --- استيراد الأدوات المساعدة ---
from utils import log_message

# --- Conditional Imports --- #
try:
    import pyewf
except ImportError:
    print("[!] Warning: pyewf not available. EWF (.E01) export will be disabled.")
    pyewf = None

# === POST-PROCESSING FUNCTIONS === #

def convert_to_ewf(args, raw_path, hashes):
    """Converts the raw image to EWF format with metadata."""
    if not pyewf:
        print("[!] pyewf not installed; skipping EWF conversion.")
        return None
    
    ewf_path = os.path.join(args.output_dir, "image.E01")
    log_file = os.path.join(args.output_dir, "acquisition.log")
    log_message(log_file, f"Starting EWF conversion to {ewf_path}")

    try:
        ewf_handle = pyewf.handle()
        ewf_handle.set_header_value("case_number", args.case_number)
        ewf_handle.set_header_value("examiner_name", args.examiner)
        ewf_handle.set_header_value("evidence_number", "1")
        ewf_handle.set_header_value("notes", f"Acquired from {args.source} on {datetime.now().isoformat()}")
        
        # Set compression and splitting
        if args.compress != 'none':
            compression_level = pyewf.compression_levels.FAST if args.compress == 'fast' else pyewf.compression_levels.BEST
            ewf_handle.set_compression_level(compression_level)
        
        if args.split > 0:
            ewf_handle.set_segment_file_size(args.split * 1024 * 1024)

        ewf_handle.open_write(ewf_path)
        ewf_handle.set_write_md5_hash(True) # Let pyewf calculate its own internal hash

        with open(raw_path, 'rb') as raw_file:
            while True:
                chunk = raw_file.read(1024 * 1024) # 1MB buffer
                if not chunk:
                    break
                ewf_handle.write(chunk)
                
        ewf_handle.close()
        log_message(log_file, "EWF conversion successful.")
        
        # Verify EWF hash if possible
        ewf_md5 = ewf_handle.get_md5_hash()
        log_message(log_file, f"EWF internal MD5: {ewf_md5}")
        
        # ملحوظة: هاش المصدر الأصلي قد يختلف لو كان هناك باد سيكتور وتم استبدالها بأصفار
        # الهاش المحسوب هنا هو للملف الـ raw الذي تم إنشاؤه
        if ewf_md5 != hashes['md5']:
            log_message(log_file, "[!] WARNING: EWF internal MD5 does not match calculated source MD5.")
            log_message(log_file, f"    Source MD5: {hashes['md5']}")
            log_message(log_file, "    (This may be OK if bad sectors were encountered)")

        return ewf_path
    except Exception as e:
        print(f"[!] EWF Conversion error: {e}")
        log_message(log_file, f"[!] EWF Conversion error: {e}")
        return None

def decrypt_bitlocker(image_path, output_dir, log_file):
    """Decrypts a BitLocker volume using dislocker."""
    mount_point = os.path.join(output_dir, "mount")
    decrypted_img = os.path.join(output_dir, "decrypted.img")
    os.makedirs(mount_point, exist_ok=True)
    
    log_message(log_file, "Attempting BitLocker decryption...")
    try:
        recovery_key = getpass.getpass(" Enter BitLocker Recovery Key: ")
        
        # استخدام dislocker-fuse
        subprocess.run([
            "dislocker", "-V", image_path, "-p" + recovery_key, "--", mount_point
        ], check=True, capture_output=True, text=True)
        
        dislocker_file = os.path.join(mount_point, "dislocker-file")
        
        if not os.path.exists(dislocker_file):
             log_message(log_file, f"[!] Error: 'dislocker-file' not found in mount point. Decryption likely failed.")
             subprocess.run(["umount", mount_point], capture_output=True) # Attempt unmount
             return None
             
        log_message(log_file, f"BitLocker volume mounted. Copying decrypted data to {decrypted_img}...")
        
        # نسخ المحتوى بدلاً من الملف الوهمي
        shutil.copyfile(dislocker_file, decrypted_img)
        
        log_message(log_file, "Decryption and copy successful.")
        
        # Unmount
        subprocess.run(["umount", mount_point], check=True)
        
        return decrypted_img
    except FileNotFoundError:
        log_message(log_file, "[!] Error: 'dislocker' command not found. Is it installed and in your PATH?")
        return None
    except subprocess.CalledProcessError as e:
        log_message(log_file, f"[!] Decryption failed. Check your recovery key or dislocker options. Error: {e.stderr}")
        return None
    except Exception as e:
        log_message(log_file, f"[!] An unexpected error occurred during decryption: {e}")
        try:
            subprocess.run(["umount", mount_point], capture_output=True) # Attempt unmount
        except:
            pass
        return None