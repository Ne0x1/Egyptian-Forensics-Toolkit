# Egyptian Forensics Framework (EFF-Toolkit)

![Version](https://img.shields.io/badge/version-v1.0-blue)
![Python Version](https://img.shields.io/badge/python-3.7+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
A project dedicated to building a trusted, open-source, and comprehensive suite of digital forensics tools developed in Egypt. This initiative aims to provide reliable, transparent, and powerful utilities for digital forensic investigators.

---

## 🚩 Module 1: Secure Disk Imager (v1.0)

This is the first module in the EFF-Toolkit: a forensically-sound disk acquisition tool written in Python. It is designed to create reliable raw (`.dd`) and EWF (`.E01`) images from source devices while ensuring data integrity.

### Key Features

* **Forensically-Sound Acquisition:** Reads the source device only once.
* **On-the-Fly Hashing:** Calculates **MD5** and **SHA256** hashes simultaneously during the imaging process.
* **Robust Bad Sector Handling:** Detects read errors, logs the bad sector's offset, and writes null bytes (`\x00`) to the destination image to maintain data offsets and integrity.
* **Software Write-Blocking:** Attempts to set the source device to **read-only** mode on Linux systems (`blockdev --setro`) to prevent evidence contamination.
* **Multiple Output Formats:**
    * Creates standard **Raw (`.dd`)** images.
    * Converts to the industry-standard **EWF (`.E01`)** format using `pyewf`.
* **EWF Metadata:** Injects critical case information (Case Number, Examiner Name, Notes) into the `.E01` file headers.
* **BitLocker Support:** Includes an experimental feature to decrypt BitLocker-encrypted volumes using `dislocker`.
* **Automated Reporting:** Generates a final **PDF report** summarizing the acquisition details, case info, and verification hashes.

---

### ⚠️ IMPORTANT WARNING ⚠️

This tool attempts to apply a **software write-block**. This is **NOT** a substitute for a physical, hardware-based write-blocker. For all evidential procedures, a hardware write-blocker is **STRONGLY** recommended. Use this tool at your own risk.

---

### Requirements

* Python 3.7+
* Root/Administrator privileges (to read block devices)
* Python libraries: `pyewf`, `reportlab`
* External tools (for optional features):
    * `dislocker` (for BitLocker decryption)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Install required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install external tools (Example on Debian/Ubuntu):**
    ```bash
    sudo apt-get update
    sudo apt-get install dislocker
    ```

---

### Usage

The script must be run as root to access block devices.

```bash
# -- (لازم تشغله بـ sudo) --
sudo python3 main.py [SOURCE_DEVICE] [OPTIONS]

Examples:

1. Basic RAW (.dd) Image with Hashing:

    Source: /dev/sdb (a USB drive)

    Output: ./case_001

    Examiner: "A. Rahman"

    Case No: "CASE-001"

Bash

sudo python3 main.py /dev/sdb -o ./case_001 -e "A. Rahman" -c "CASE-001"

2. Create an EWF (.E01) Image with Compression and Splitting:

    Creates a compressed .E01 image, split into 2GB (2048MB) files.

Bash

sudo python3 main.py /dev/sdc -o ./case_002 -e "A. Rahman" --ewf --split 2048 --compress best

3. Attempt BitLocker Decryption on an Image File:

    Source: encrypted_image.dd (a file, not a device)

Bash

sudo python3 main.py ./encrypted_image.dd -o ./decrypted_case --bitlocker

(You will be prompted for the BitLocker recovery key).

🚀 Project Roadmap (Future Goals)

This is just the beginning. The vision for the Egyptian Forensics Framework includes:

    [Module 2: Memory Forensics]

        v2.0: A cross-platform memory acquisition tool (using drivers/LKM).

        v2.1: A memory analysis engine (Python-based, inspired by Volatility) to parse memory dumps for processes, network connections, and artifacts.

    [Module 3: Triage & Artifacts]

        A tool for rapid collection of critical artifacts (Event Logs, Registry, Prefetch, etc.) from live systems.

    [The Framework GUI]

        A final GUI (using PyQt/Tkinter) to unify all CLI modules into a single, user-friendly application.

Author

    AbdelrahmanELsayed (Ne0x1)
    LikedIN : https://www.linkedin.com/in/abdelrahman-elsayed-1a31b4300
    GITHUB : https://github.com/Ne0x1
    
