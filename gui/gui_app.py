import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import deps_check
deps_check.ensure_dependencies()

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import os
import smtplib
from email.message import EmailMessage
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter

class CertificateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Mailer Automation")
        self.root.geometry("800x800")
        
        self.template_path = None
        self.create_widgets()

    def create_widgets(self):
        # --- Template Section ---
        frame_template = tk.LabelFrame(self.root, text="1. Certificate Template (PDF)", padx=10, pady=10)
        frame_template.pack(fill="x", padx=10, pady=5)
        
        self.btn_browse = tk.Button(frame_template, text="Select PDF Template", command=self.browse_template)
        self.btn_browse.pack(side="left")
        
        self.lbl_template = tk.Label(frame_template, text="No file selected")
        self.lbl_template.pack(side="left", padx=10)
        
        tk.Label(frame_template, text="Font Size:").pack(side="left", padx=(20, 5))
        self.entry_font_size = tk.Entry(frame_template, width=5)
        self.entry_font_size.insert(0, "40")
        self.entry_font_size.pack(side="left")
        
        tk.Label(frame_template, text="Y-Offset (from center):").pack(side="left", padx=(20, 5))
        self.entry_y_offset = tk.Entry(frame_template, width=5)
        self.entry_y_offset.insert(0, "0")
        self.entry_y_offset.pack(side="left")
        
        tk.Label(frame_template, text="X-Offset:").pack(side="left", padx=(20, 5))
        self.entry_x_offset = tk.Entry(frame_template, width=5)
        self.entry_x_offset.insert(0, "0")
        self.entry_x_offset.pack(side="left")
        
        # --- Data Section ---
        frame_data = tk.LabelFrame(self.root, text="2. Students Data (Paste Name, Email - one per line)", padx=10, pady=10)
        frame_data.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_data = scrolledtext.ScrolledText(frame_data, height=8)
        self.txt_data.pack(fill="both", expand=True)
        self.txt_data.insert(tk.END, "John Doe, john@example.com\nJane Smith, jane@example.com")
        
        # --- Email Settings ---
        frame_email = tk.LabelFrame(self.root, text="3. Email Settings", padx=10, pady=10)
        frame_email.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_email, text="Your Gmail:").grid(row=0, column=0, sticky="e", pady=2)
        self.entry_email = tk.Entry(frame_email, width=40)
        self.entry_email.grid(row=0, column=1, pady=2, sticky="w")
        
        tk.Label(frame_email, text="App Password:").grid(row=1, column=0, sticky="e", pady=2)
        self.entry_password = tk.Entry(frame_email, width=40, show="*")
        self.entry_password.grid(row=1, column=1, pady=2, sticky="w")
        
        tk.Label(frame_email, text="Subject:").grid(row=2, column=0, sticky="e", pady=2)
        self.entry_subject = tk.Entry(frame_email, width=60)
        self.entry_subject.insert(0, "Your Certificate of Participation")
        self.entry_subject.grid(row=2, column=1, pady=2, sticky="w")
        
        tk.Label(frame_email, text="Body (use {name} for student name):").grid(row=3, column=0, sticky="ne", pady=2)
        self.txt_body = scrolledtext.ScrolledText(frame_email, height=6, width=60)
        self.txt_body.grid(row=3, column=1, pady=2, sticky="w")
        self.txt_body.insert(tk.END, "Hello {name},\n\nPlease find your certificate attached.\n\nBest,\nThe Team")
        
        # --- Action Section ---
        frame_action = tk.Frame(self.root, padx=10, pady=10)
        frame_action.pack(fill="x")
        
        self.btn_run = tk.Button(frame_action, text="GENERATE & SEND EMAILS", bg="green", fg="white", font=("Arial", 12, "bold"), command=self.start_process)
        self.btn_run.pack(fill="x", ipady=10)
        
        # --- Log Section ---
        frame_log = tk.LabelFrame(self.root, text="Logs", padx=10, pady=10)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_log = scrolledtext.ScrolledText(frame_log, height=8, state='disabled')
        self.txt_log.pack(fill="both", expand=True)

    def log(self, message):
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')
        self.root.update_idletasks()

    def browse_template(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.template_path = file_path
            self.lbl_template.config(text=os.path.basename(file_path))

    def start_process(self):
        if not self.template_path:
            messagebox.showerror("Error", "Please select a PDF template.")
            return
            
        data_text = self.txt_data.get("1.0", tk.END).strip()
        if not data_text:
            messagebox.showerror("Error", "Please provide student data.")
            return
            
        # Disable button during process
        self.btn_run.config(state="disabled")
        
        # Run in thread
        threading.Thread(target=self.process_task, daemon=True).start()

    def process_task(self):
        try:
            self.log("Starting process...")
            
            # Setup output dir
            output_dir = "certificates_out"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # Parse parameters
            font_size = int(self.entry_font_size.get())
            y_offset = float(self.entry_y_offset.get())
            x_offset = float(self.entry_x_offset.get())
            
            sender_email = self.entry_email.get().strip()
            sender_password = self.entry_password.get().strip()
            subject = self.entry_subject.get().strip()
            body_template = self.txt_body.get("1.0", tk.END).strip()
            
            # Parse data
            data_text = self.txt_data.get("1.0", tk.END).strip()
            students = []
            for line in data_text.split('\n'):
                line = line.strip()
                if not line: continue
                parts = line.split(',')
                if len(parts) >= 2:
                    students.append((parts[0].strip(), parts[1].strip()))
                else:
                    self.log(f"Skipping invalid line: {line}")
            
            self.log(f"Found {len(students)} students to process.")
            
            success_count = 0
            
            for name, email in students:
                self.log(f"\nProcessing {name}...")
                
                # 1. Generate PDF
                cert_filename = f"{name.replace(' ', '_')}_certificate.pdf"
                cert_path = os.path.join(output_dir, cert_filename)
                
                # Overlay text on PDF
                reader = PdfReader(self.template_path)
                page = reader.pages[0]
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                
                # Calculate center position
                center_x = (page_width / 2.0) + x_offset
                center_y = (page_height / 2.0) + y_offset
                
                can.setFont("Helvetica-Bold", font_size)
                can.drawCentredString(center_x, center_y, name)
                can.save()
                
                packet.seek(0)
                new_pdf = PdfReader(packet)
                
                writer = PdfWriter()
                page.merge_page(new_pdf.pages[0])
                writer.add_page(page)
                
                with open(cert_path, "wb") as f_out:
                    writer.write(f_out)
                    
                self.log(f"Generated {cert_filename}")
                
                # 2. Send Email
                if not sender_email or not sender_password:
                    self.log("No email credentials provided. Skipping email send.")
                    continue
                    
                self.log(f"Sending email to {email}...")
                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = email
                msg.set_content(body_template.format(name=name))
                
                with open(cert_path, 'rb') as f_cert:
                    msg.add_attachment(f_cert.read(), maintype='application', subtype='pdf', filename=cert_filename)
                
                try:
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                    self.log(f"Successfully sent email to {email}")
                    success_count += 1
                except Exception as e:
                    self.log(f"Failed to send email to {email}: {str(e)}")
                    
            self.log(f"\n--- DONE ---")
            self.log(f"Successfully sent {success_count} emails out of {len(students)}")
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
        finally:
            self.btn_run.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateApp(root)
    root.mainloop()
