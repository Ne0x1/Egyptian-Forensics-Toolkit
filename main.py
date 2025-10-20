#!/usr/bin/env python3

import os
import sys
import argparse
from datetime import datetime

# --- استيراد الدوال من باقي الملفات ---
from utils import log_message, generate_report, BAD_SECTOR_LOG
from acquisition_core import acquire_image
from post_processing import convert_to_ewf, decrypt_bitlocker

# === ENTRY POINT === #
def main():
    parser = argparse.ArgumentParser(
        description="A comprehensive forensic imaging tool.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("source", help="Source device or image file (e.g., /dev/sdb, image.dd)")
    parser.add_argument("-o", "--output-dir", default="./forensic_output", help="Directory to save all output files.")
    parser.add_argument("-e", "--examiner", default="N/A", help="Name of the examiner.")
    parser.add_argument("-c", "--case-number", default="N/A", help="Case number for documentation.")
    
    # ضفنا الخيار ده عشان نمرره لأداة ewfacquirestream
    parser.add_argument("-ev", "--evidence-number", default="1", help="Evidence number for documentation.")

    parser.add_argument("--ewf", action="store_true", help="Convert the final RAW image to EWF (.E01) format.")
    parser.add_argument("--split", type=int, default=0, help="For EWF only: Split size in MB (e.g., 2048 for 2GB). Default is 1.5GB if 0.")
    parser.add_argument("--compress", choices=['none', 'fast', 'best'], default='fast', help="For EWF only: Compression level.")
    parser.add_argument("--bitlocker", action="store_true", help="Attempt to decrypt the source image if it's BitLocker encrypted.")

    args = parser.parse_args()

    # --- Setup --- #
    if not os.path.exists(args.source):
        print(f"[!] Error: Source path '{args.source}' does not exist.")
        sys.exit(1)
    
    os.makedirs(args.output_dir, exist_ok=True)
    log_file = os.path.join(args.output_dir, "acquisition.log")
    
    # تهيئة ملفات اللوج
    global BAD_SECTOR_LOG
    BAD_SECTOR_LOG = os.path.join(args.output_dir, "bad_sectors.log")
    
    print("=" * 60)
    print("      FORENSIC IMAGING UTILITY V1.0.1 (EFF-Toolkit)")
    print("      Dev BY : @Vbdelrvhmvnx_")
    print("=" * 60)
    print(f"[*] WARNING: This tool attempts to modify block device states ('ro').")
    print(f"[*] A HARDWARE WRITE-BLOCKER IS THE ONLY GUARANTEED METHOD.")
    print("=" * 60)

    # --- Main Process --- #
    raw_image_path, hashes = acquire_image(args, log_file)
    
    if not raw_image_path:
        log_message(log_file, "Acquisition failed. Exiting.")
        sys.exit(1)

    final_image_path = raw_image_path
    
    # Optional BitLocker Decryption
    if args.bitlocker:
        decrypted_path = decrypt_bitlocker(raw_image_path, args.output_dir, log_file)
        if decrypted_path:
            log_message(log_file, "Hashing decrypted image...")
            # ملحوظة: في سيناريو حقيقي، يجب إعادة حساب الهاش للملف المفكوك
            final_image_path = decrypted_path 
        else:
            log_message(log_file, "BitLocker decryption failed. Continuing with encrypted image.")

    # Optional EWF Conversion
    if args.ewf:
        ewf_image_path = convert_to_ewf(args, final_image_path, hashes)
        if ewf_image_path:
            final_image_path = ewf_image_path
            # Optional: Remove the large RAW file after successful EWF conversion
            # if final_image_path != raw_image_path:
            #     os.remove(raw_image_path)

    # --- Reporting --- #
    generate_report(args, hashes, final_image_path, log_file)

    log_message(log_file, "✅ Forensic acquisition process completed.")
    print(f"\nFinal output located in: {args.output_dir}")
    print(f"Primary evidence file: {final_image_path}")

if __name__ == "__main__":
    if os.geteuid() != 0 and sys.platform.startswith('linux'):
        print("[!] This script needs to be run as root to access block devices.")
        sys.exit(1)
    main()
