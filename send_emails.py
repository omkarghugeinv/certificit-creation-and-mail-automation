import os
import smtplib
from email.message import EmailMessage
import mimetypes

def send_email_with_attachment(sender_email, sender_password, recipient_email, subject, body, attachment_path, smtp_server='smtp.gmail.com', smtp_port=587):
    """Sends an email with a file attachment via SMTP."""
    
    if not recipient_email:
        print("Skipping email send: No recipient email provided.")
        return False
        
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)

    # Attach the certificate
    if os.path.exists(attachment_path):
        ctype, encoding = mimetypes.guess_type(attachment_path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        
        with open(attachment_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))
    else:
        print(f"Attachment {attachment_path} not found.")
        return False

    try:
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Successfully sent email to {recipient_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False
