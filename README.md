# Certificate Creation and Mail Automation

This project provides tools to automatically generate certificates for students/participants and email them as PDF attachments. It includes both a Command-Line Interface (CLI) and a Graphical User Interface (GUI).

## Features
- Generate certificates by overlaying names onto a template.
- Automatically email the generated certificates as PDF attachments to a list of recipients.
- Personalize the email body for each recipient.
- Supports both GUI (for easy point-and-click) and CLI (for terminal users).

## Prerequisites

Make sure you have Python installed. Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## How to Use the GUI (No Python Required)
If you don't want to install Python, you can directly run the standalone executable:
1. Navigate to the `dist/` folder.
2. Double-click **`CertificateMailerGUI.exe`**.

## How to Use the GUI (For Developers)
If you have Python installed and want to run it from the source code:

1. Double click the `run_gui.bat` file, or run the following command in your terminal:
   ```bash
   cd gui
   python gui_app.py
   ```
2. Select your base PDF template.
3. Paste your student data in the format: `Name, Email` (one per line).
4. Enter your Gmail address and **App Password**.
5. Customize your subject and body (you can use `{name}` as a placeholder for the student's name).
6. Click **GENERATE & SEND EMAILS**.

## How to Use the CLI
If you prefer the command line:

1. Add your student data to `cli/students.csv`.
2. Make sure you have your template ready (e.g., `cli/template.png`).
3. Run the following command:
   ```bash
   cd cli
   python main.py
   ```
4. Follow the on-screen prompts to configure email settings and send the certificates.

## Important Note on Gmail App Passwords
If you are using a Gmail account to send these emails, you cannot use your regular account password due to security restrictions. You must generate an **App Password**:
1. Go to your Google Account > Security.
2. Enable 2-Step Verification.
3. Search for "App Passwords" and create a new one for this application.
4. Use that 16-character password in the app.
