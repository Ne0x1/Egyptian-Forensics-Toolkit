# 🇪🇬 Egyptian Forensics Framework (EFF-Toolkit)

![Version](https://img.shields.io/badge/version-v1.0.1-blue)
![Python](https://img.shields.io/badge/python-3.7+-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
![DFIR](https://img.shields.io/badge/DFIR-Toolkit-red)

---

## 📌 Overview

Egyptian Forensics Framework (EFF-Toolkit) is an open-source initiative aimed at building a trusted, scalable, and forensically-sound DFIR toolkit developed in Egypt 🇪🇬.

The goal is to provide:
- Reliable forensic acquisition tools  
- Modular DFIR capabilities  
- Enterprise-level investigation workflows  

---

# 🚩 Module 1: Secure Disk Imager (v1.0.1)

A forensically sound disk acquisition tool written in Python.

Supports:
- Raw images (.dd)
- EWF format (.E01)

Ensures:
- Data integrity
- Evidence reliability

---

## ✨ Key Features

### 🧪 Forensic Integrity
- Reads source device only once  
- Prevents contamination  

### 🔐 Hashing
- MD5  
- SHA256  

### 💥 Bad Sector Handling
- Detects errors  
- Logs offsets  
- Writes null bytes  

### 🛡️ Write Blocking
- Software-based read-only enforcement  

### 📦 EWF Support
- Uses ewfacquirestream  
- Embeds metadata  

### 🔓 BitLocker Support
- Uses dislocker  

### 📄 Reporting
- Generates PDF reports  

---

## ⚠️ IMPORTANT WARNING

This tool uses software-based write blocking.  
This is NOT a replacement for hardware write blockers.

---

## 🧰 Requirements

### System Dependencies

```bash
sudo apt update
sudo apt install ewf-tools dislocker python3-venv
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Ne0x1/Egyptian-Forensics-Toolkit.git
cd Egyptian-Forensics-Toolkit

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 Usage

⚠️ Do NOT run:
```bash
sudo python3 main.py
```

✅ Correct:
```bash
sudo venv/bin/python main.py [SOURCE_DEVICE] [OPTIONS]
```

---

## 📌 Examples

### RAW Image
```bash
sudo venv/bin/python main.py /dev/sdb -o ./case_001 -e "A. Rahman" -c "CASE-001"
```

### EWF Image
```bash
sudo venv/bin/python main.py /dev/sdc -o ./case_002 -e "A. Rahman" -c "CASE-002" --ewf --compress best
```

---

## 🧠 Architecture

[Source Device] → [Read Engine] → [Hash Engine] → [Error Handler] → [Output Writer] → [Report Generator]

---

## 🔍 DFIR Value

- Digital Forensics  
- Incident Response  
- Evidence Preservation  
- Legal investigations  

---

## 🔐 Security Considerations

- Requires root access  
- Use in trusted environments  
- Avoid production misuse  

---

## 🗺️ Roadmap

### Module 2: Memory Forensics
- Memory acquisition  
- Memory analysis  

### Module 3: Triage
- Artifact collection  

### GUI
- Unified interface  

---

## 💡 Future Work

- Multi-threading  
- Remote acquisition  
- Timeline analysis  

---

## 👨‍💻 Author

Abdelrahman Elsayed  
GitHub: https://github.com/Ne0x1  
LinkedIn: https://www.linkedin.com/in/abdelrahman-elsayed-1a31b4300  

---

## 📜 License

MIT License
