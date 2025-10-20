import os
from datetime import datetime

# --- Conditional Imports --- #
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    print("[!] Warning: ReportLab missing. PDF Report generation will be disabled.")
    canvas = None

# === GLOBAL CONFIGURATION === #
# سيتم تحديث هذا المتغير من main.py عند بدء التشغيل
BAD_SECTOR_LOG = "bad_sectors.log"

# === HELPER FUNCTIONS === #

def log_message(log_file, message):
    """Appends a timestamped message to the main log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    try:
        with open(log_file, 'a') as f:
            f.write(full_message + '\n')
    except Exception as e:
        print(f"[!] Critical log write error: {e}")

def generate_report(args, hashes, final_image_path, log_file_path):
    """Generates a simple PDF report of the acquisition."""
    if not canvas:
        log_message(log_file_path, "ReportLab not found. Skipping PDF report generation.")
        return
    
    report_path = os.path.join(args.output_dir, "acquisition_report.pdf")

    try:
        c = canvas.Canvas(report_path, pagesize=letter)
        width, height = letter
        
        # إعدادات الخطوط
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 50, "Forensic Acquisition Report")
        
        c.setFont("Helvetica", 12)
        
        # إحداثيات البداية
        x_margin = 72
        y_current = height - 100
        line_height = 18

        def draw_line(label, value, is_wrap=False):
            nonlocal y_current
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_margin, y_current, label)
            c.setFont("Helvetica", 12)
            if is_wrap:
                # للكتابة الطويلة مثل مسارات الملفات
                c.drawString(x_margin + 120, y_current, value) # بداية النص
            else:
                c.drawString(x_margin + 120, y_current, str(value))
            y_current -= line_height

        # بيانات القضية
        draw_line("Case Number:", args.case_number)
        draw_line("Examiner:", args.examiner)
        draw_line("Timestamp (UTC):", f"{datetime.utcnow().isoformat()}Z")
        y_current -= line_height # مسافة

        # بيانات الدليل
        draw_line("Source Device:", args.source, is_wrap=True)
        draw_line("Final Image Path:", final_image_path, is_wrap=True)
        y_current -= line_height # مسافة
        
        # الهاش
        draw_line("MD5 Hash:", hashes.get('md5', 'N/A'))
        draw_line("SHA256 Hash:", hashes.get('sha256', 'N/A'))
        y_current -= line_height # مسافة

        # تضمين اللوج
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y_current, "Acquisition Log:")
        c.setFont("Helvetica", 9) # خط أصغر للوج
        y_current -= (line_height * 1.2)
        
        try:
            with open(log_file_path, 'r') as f:
                for line in f:
                    if y_current < 50: # لو الصفحة خلصت
                        c.showPage() # اعمل صفحة جديدة
                        c.setFont("Helvetica", 9)
                        y_current = height - 50 # ابدأ من فوق
                    
                    c.drawString(x_margin, y_current, line.strip())
                    y_current -= 12 # مسافة أصغر بين سطور اللوج
        except Exception as e:
            c.drawString(x_margin, y_current, f"Could not read log file: {e}")
            
        c.save()
        log_message(log_file_path, f"[+] Report generated at {report_path}")
    except Exception as e:
        log_message(log_file_path, f"[!] Report generation failed: {e}")