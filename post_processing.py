import os
import getpass
import subprocess
import shutil
from datetime import datetime

# --- استيراد الأدوات المساعدة ---
from utils import log_message

# === POST-PROCESSING FUNCTIONS === #

def convert_to_ewf(args, raw_path, hashes):
    """
    Converts the raw image to EWF format using the 'ewfacquirestream' command-line tool.
    This is more reliable than the Python bindings for writing metadata.
    """
    ewf_path = os.path.join(args.output_dir, "image.E01")
    log_file = os.path.join(args.output_dir, "acquisition.log")
    log_message(log_file, f"Starting EWF conversion to {ewf_path} using 'ewfacquirestream'...")

    # --- 1. جهز الأوامر ---
    split_size_bytes = args.split * 1024 * 1024
    
    compression_map = {
        'none': 'empty-block',
        'fast': 'fast',
        'best': 'bzip2'
    }
    compression_type = compression_map.get(args.compress, 'fast')

    # استخدمنا args.evidence_number اللي ضفناه في main.py
    command = [
        "ewfacquirestream",
        "-C", args.case_number,
        "-E", args.evidence_number,
        "-e", args.examiner,
        "-N", f"Acquired from {args.source}",
        "-c", compression_type,
        "-S", str(split_size_bytes) if split_size_bytes > 0 else "0",
        "-t", ewf_path
    ]
    
    log_message(log_file, f"Executing command: {' '.join(command)}")

    # --- 2. نفذ الأمر واعمل "Pipe" للملف ---
    try:
        with open(raw_path, 'rb') as raw_file:
            process = subprocess.Popen(
                command,
                stdin=raw_file,     # الـ input هو الملف الـ raw
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                log_message(log_file, f"[!] ewfacquirestream failed!")
                log_message(log_file, f"    STDOUT: {stdout}")
                log_message(log_file, f"    STDERR: {stderr}")
                return None
            
            log_message(log_file, "EWF conversion successful.")
            log_message(log_file, f"    {stderr.strip()}") # بنطبع الهاش اللي الأداة طلعته

            return ewf_path

    except FileNotFoundError:
        log_message(log_file, "[!] Error: 'ewfacquirestream' command not found.")
        log_message(log_file, "    Please install it using (Debian/Parrot): sudo apt install ewf-tools")
        return None
    except Exception as e:
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
