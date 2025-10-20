# Egyptian Forensics Framework (EFF-Toolkit)

![Version](https://img.shields.io/badge/version-v1.0.1-blue)
![Python Version](https://img.shields.io/badge/python-3.7+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)

A project dedicated to building a trusted, open-source, and comprehensive suite of digital forensics tools developed in Egypt.

---

## 🚩 Module 1: Secure Disk Imager (v1.0.1)

This is the first module in the EFF-Toolkit: a forensically-sound disk acquisition tool written in Python. It is designed to create reliable raw (`.dd`) and EWF (`.E01`) images from source devices while ensuring data integrity.

### Key Features

* **Forensically-Sound Acquisition:** Reads the source device only once.
* **On-the-Fly Hashing:** Calculates **MD5** and **SHA256** simultaneously during the imaging process.
* **Robust Bad Sector Handling:** Detects read errors, logs the offset, and writes null bytes (`\x00`).
* **Software Write-Blocking:** Attempts to set the source device to **read-only** mode on Linux.
* **EWF `.E01` Support:** Uses the official **`ewfacquirestream`** utility (from `ewf-tools`) to create forensically-sound EWF files, embedding all case metadata (Case No, Examiner, etc.).
* **BitLocker Support:** Experimental decryption using `dislocker`.
* **Automated Reporting:** Generates a final **PDF report** summarizing the acquisition.

---

### ⚠️ IMPORTANT WARNING ⚠️

This tool attempts to apply a **software write-block**. This is **NOT** a substitute for a physical, hardware-based write-blocker. For all evidential procedures, a hardware write-blocker is **STRONGLY** recommended. Use this tool at your own risk.

---

### Requirements

This tool has two types of dependencies: **System Tools** and **Python Libraries**.

**1. System Tools (Required):**
You must install these on your system (e.g., ParrotOS, Ubuntu, Debian).
* `ewf-tools`: (Provides `ewfacquirestream` for EWF conversion)
* `dislocker`: (Provides `dislocker` for BitLocker decryption)
* `python3-venv`: (Provides the ability to create virtual environments)

**2. Python Libraries (Required):**
These will be installed *inside* the virtual environment.
* `reportlab`: (For generating PDF reports)

---

### Installation

**Step 1: Install System Dependencies**
(Example on Debian/Ubuntu/ParrotOS)
```bash
sudo apt update
sudo apt install ewf-tools dislocker python3-venv

Step 2: Clone the Repository

git clone [https://github.com/Ne0x1/Egyptian-Forensics-Toolkit.git](https://github.com/Ne0x1/Egyptian-Forensics-Toolkit.git)
cd Egyptian-Forensics-Toolkit
Step 3: Create and Activate a Virtual Environment (CRITICAL STEP)

It is highly recommended to use a Virtual Environment (venv) to avoid conflicts with your system's Python packages.
Bash

# Create the venv
python3 -m venv venv

# Activate the venv
source venv/bin/activate

(Your terminal prompt should now start with (venv))

Step 4: Install Python Requirements While the venv is active, install the libraries from requirements.txt:
Bash

pip install -r requirements.txt

Usage

Because this tool needs root privileges (to read devices like /dev/sdb) and also needs to use the Python libraries inside your venv, you must run it in a specific way.

DO NOT just run sudo python3 main.py. This will use the system's Python and fail.

The Correct Way (SUDO + VENV): Call the python executable inside your venv folder using sudo.
Bash

# -- (الصيغة الصحيحة) --
sudo venv/bin/python main.py [SOURCE_DEVICE] [OPTIONS]

Examples:

1. Basic RAW (.dd) Image:
Bash

sudo venv/bin/python main.py /dev/sdb -o ./case_001 -e "A. Rahman" -c "CASE-001" -ev "1-A"

2. Create a Compressed EWF (.E01) Image:
Bash

sudo venv/bin/python main.py /dev/sdc -o ./case_002 -e "A. Rahman" -c "CASE-002" --ewf --compress best

🚀 Project Roadmap (Future Goals)

This is just the beginning. The vision for the Egyptian Forensics Framework includes:

    [Module 2: Memory Forensics]

        v2.0: A cross-platform memory acquisition tool (using drivers/LKM).

        v2.1: A memory analysis engine (Python-based, inspired by Volatility) to parse memory dumps.

    [Module 3: Triage & Artifacts]

        A tool for rapid collection of critical artifacts from live systems.

    [The Framework GUI]

        A final GUI to unify all CLI modules into a single, user-friendly application.


README.md 
Markdown

# Egyptian Forensics Framework (EFF-Toolkit)

![Version](https://img.shields.io/badge/version-v1.0.1-blue)
![Python Version](https://img.shields.io/badge/python-3.7+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)

A project dedicated to building a trusted, open-source, and comprehensive suite of digital forensics tools developed in Egypt.

---

## 🚩 Module 1: Secure Disk Imager (v1.0.1)

This is the first module in the EFF-Toolkit: a forensically-sound disk acquisition tool written in Python. It is designed to create reliable raw (`.dd`) and EWF (`.E01`) images from source devices while ensuring data integrity.

### Key Features

* **Forensically-Sound Acquisition:** Reads the source device only once.
* **On-the-Fly Hashing:** Calculates **MD5** and **SHA256** simultaneously during the imaging process.
* **Robust Bad Sector Handling:** Detects read errors, logs the offset, and writes null bytes (`\x00`).
* **Software Write-Blocking:** Attempts to set the source device to **read-only** mode on Linux.
* **EWF `.E01` Support:** Uses the official **`ewfacquirestream`** utility (from `ewf-tools`) to create forensically-sound EWF files, embedding all case metadata (Case No, Examiner, etc.).
* **BitLocker Support:** Experimental decryption using `dislocker`.
* **Automated Reporting:** Generates a final **PDF report** summarizing the acquisition.

---

### ⚠️ IMPORTANT WARNING ⚠️

This tool attempts to apply a **software write-block**. This is **NOT** a substitute for a physical, hardware-based write-blocker. For all evidential procedures, a hardware write-blocker is **STRONGLY** recommended. Use this tool at your own risk.

---

### Requirements

This tool has two types of dependencies: **System Tools** and **Python Libraries**.

**1. System Tools (Required):**
You must install these on your system (e.g., ParrotOS, Ubuntu, Debian).
* `ewf-tools`: (Provides `ewfacquirestream` for EWF conversion)
* `dislocker`: (Provides `dislocker` for BitLocker decryption)
* `python3-venv`: (Provides the ability to create virtual environments)

**2. Python Libraries (Required):**
These will be installed *inside* the virtual environment.
* `reportlab`: (For generating PDF reports)

---

### Installation

**Step 1: Install System Dependencies**
(Example on Debian/Ubuntu/ParrotOS)
```bash
sudo apt update
sudo apt install ewf-tools dislocker python3-venv

Step 2: Clone the Repository
Bash

git clone [https://github.com/Ne0x1/Egyptian-Forensics-Toolkit.git](https://github.com/Ne0x1/Egyptian-Forensics-Toolkit.git)
cd Egyptian-Forensics-Toolkit

Step 3: Create and Activate a Virtual Environment (CRITICAL STEP)

It is highly recommended to use a Virtual Environment (venv) to avoid conflicts with your system's Python packages.
Bash

# Create the venv
python3 -m venv venv

# Activate the venv
source venv/bin/activate

(Your terminal prompt should now start with (venv))

Step 4: Install Python Requirements While the venv is active, install the libraries from requirements.txt:
Bash

pip install -r requirements.txt


Usage


Because this tool needs root privileges (to read devices like /dev/sdb) and also needs to use the Python libraries inside your venv, you must run it in a specific way.

DO NOT just run sudo python3 main.py. This will use the system's Python and fail.

The Correct Way (SUDO + VENV): Call the python executable inside your venv folder using sudo.
Bash

# -- (الصيغة الصحيحة) --
sudo venv/bin/python main.py [SOURCE_DEVICE] [OPTIONS]

Examples:

1. Basic RAW (.dd) Image:
Bash

sudo venv/bin/python main.py /dev/sdb -o ./case_001 -e "A. Rahman" -c "CASE-001" -ev "1-A"

2. Create a Compressed EWF (.E01) Image:
Bash

sudo venv/bin/python main.py /dev/sdc -o ./case_002 -e "A. Rahman" -c "CASE-002" --ewf --compress best

🚀 Project Roadmap (Future Goals)

This is just the beginning. The vision for the Egyptian Forensics Framework includes:

    [Module 2: Memory Forensics]

        v2.0: A cross-platform memory acquisition tool (using drivers/LKM).

        v2.1: A memory analysis engine (Python-based, inspired by Volatility) to parse memory dumps.

    [Module 3: Triage & Artifacts]

        A tool for rapid collection of critical artifacts from live systems.

    [The Framework GUI]

        A final GUI to unify all CLI modules into a single, user-friendly application.

Author 

    Abdelrahman (@Ne0x1)
    https://www.linkedin.com/in/abdelrahman-elsayed-1a31b4300
    https://github.com/Ne0x1
