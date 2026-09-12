import deps_check
deps_check.ensure_dependencies()

import os
import getpass
from generate_certificates import generate_certificates
from send_emails import send_email_with_attachment

def main():
    print("=== Certificate Generator & Mail Automation ===")
    
    # 1. Generate Certificates
    print("\n[Step 1] Generating Certificates...")
    generated_data = generate_certificates('students.csv', 'template.png', 'certificates')
    
    if not generated_data:
        print("No certificates were generated. Please check your students.csv.")
        return
        
    print(f"\nSuccessfully generated {len(generated_data)} certificates.")
    
    # 2. Ask for Email Configuration
    print("\n[Step 2] Email Configuration")
    send_mails = input("Do you want to send these certificates via email now? (y/n): ").strip().lower()
    
    if send_mails != 'y':
        print("Certificates generated and saved in 'certificates' folder. Exiting.")
        return
        
    print("\nPlease enter your email credentials.")
    print("Note: If using Gmail, use an 'App Password' instead of your real password.")
    sender_email = input("Sender Email Address: ").strip()
    sender_password = getpass.getpass("App Password: ").strip()
    
    subject = input("Email Subject (default: 'Your Certificate of Participation'): ").strip()
    if not subject:
        subject = "Your Certificate of Participation"
        
    print("\nEnter email body. You can use '{name}' as a placeholder which will be replaced with the student's name.")
    print("Default body will be used if left empty.")
    body_input = input("Email Body: ").strip()
    
    if not body_input:
        body_template = "Hello {name},\n\nPlease find your certificate of participation attached.\n\nBest regards,\nThe Team"
    else:
        body_template = body_input
    
    # 3. Send Emails
    print("\n[Step 3] Sending Emails...")
    success_count = 0
    fail_count = 0
    
    for data in generated_data:
        name = data['name']
        email = data['email']
        cert_path = data['cert_path']
        
        if not email:
            print(f"Skipping {name} - no email provided.")
            fail_count += 1
            continue
            
        personalized_body = body_template.format(name=name)
        
        print(f"Sending to {name} ({email})...")
        success = send_email_with_attachment(
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=email,
            subject=subject,
            body=personalized_body,
            attachment_path=cert_path
        )
        
        if success:
            success_count += 1
        else:
            fail_count += 1
            
    print("\n=== Summary ===")
    print(f"Total Sent: {success_count}")
    print(f"Total Failed/Skipped: {fail_count}")

if __name__ == "__main__":
    main()
