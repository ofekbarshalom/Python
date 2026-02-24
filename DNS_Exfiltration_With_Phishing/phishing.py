# ofek bar-shalom & Yakir Litmanovitch

import re
import requests
import smtplib
from email.message import EmailMessage
from pathlib import Path


# Send email with optional file attachment
def send_email(subject, message, recipient_email, attachment_path=None):
    sender_email = "test@example.com"
    smtp_server = "localhost"
    smtp_port = 1025

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    if attachment_path:
        try:
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = Path(attachment_path).name
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        except Exception as e:
            print(f"[!] Failed to attach file: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.send_message(msg)
            print("[+] Email sent")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")


# Choose template source (URL, file, string, or adaptive)
def load_email_pattern():
    print("\nHow would you like to provide the email pattern/style?")
    print("1. From a URL")
    print("2. From a .txt file")
    print("3. Enter a string manually")
    print("4. Use the default phishing email")

    choice = input("Enter option number (1/2/3/4): ").strip()

    if choice == '1':
        return generate_email_from_url()
    elif choice == '2':
        return generate_email_from_file()
    elif choice == '3':
        return generate_email_from_string()
    elif choice == '4':
        return generate_default_phishing_email()
    else:
        print("Invalid choice. Using default template.")
        return generate_default_phishing_email()


# Load template from URL
def generate_email_from_url():
    url = input("Enter the URL of the email template: ").strip()
    try:
        response = requests.get(url)
        response.raise_for_status()
        template = response.text
        return fill_template_and_extract_subject(template, prompt_user_replacements())
    except Exception as e:
        print(f"[-] Failed to fetch template from URL: {e}")
        return "Security Alert", "Could not load template."


# Load template from file and ask for all required values
def generate_email_from_file():
    filepath = input("Enter path to .txt file: ").strip()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            template = file.read()
            return fill_template_and_extract_subject(template, prompt_user_replacements())
    except FileNotFoundError:
        print("[-] File not found.")
        return "Security Alert", "Could not load template."


# Manual input of template string
def generate_email_from_string():
    print("Paste your custom email content below (use {download_link} if needed):")
    user_input = input()
    if not user_input.strip():
        print("[-] Empty template. Using fallback.")
        return "Security Alert", "Template was empty."
    return fill_template_and_extract_subject(user_input, prompt_user_replacements())


# Ask user for all values required to fill the template
def prompt_user_replacements():
    username = input("Enter your full name: ").strip().title()
    mail_service = input("Mail service name (e.g., Gmail, Outlook): ").strip()
    title = input("Title (Mr., Ms., Dr., etc.): ").strip().title()
    job_title = input("Job title: ").strip().title()
    personal_status = input("Marital status (e.g., Married, Single): ").strip()
    kids_info = input("Kids info (ages or leave blank): ").strip()
    download_link = input("Enter download link (optional): ").strip()

    # Format kids_info nicely
    numbers = re.findall(r'\d+', kids_info)
    if numbers:
        if len(numbers) == 1:
            kids_info = f"and a parent of a child aged {numbers[0]}"
        elif len(numbers) == 2:
            kids_info = f"and a parent of children aged {numbers[0]} and {numbers[1]}"
        else:
            kids_info = f"and a parent of children aged {', '.join(numbers[:-1])} and {numbers[-1]}"
    else:
        kids_info = ""

    return {
        'username': username,
        'mail_service': mail_service,
        'title': title,
        'job_title': job_title,
        'personal_status': personal_status,
        'kids_info': kids_info,
        'download_link': download_link
    }


# Choose template file based on personal profile
def choose_template(personal_status, kids_info):
    if personal_status.lower() == 'single' and not kids_info:
        return "templates/template_single_no_kids.txt"
    elif personal_status.lower() == 'married' and kids_info:
        return "templates/template_married_with_kids.txt"
    elif personal_status.lower() == 'married':
        return "templates/template_married_no_kids.txt"
    else:
        return "templates/template_generic.txt"


# Fill placeholders in template and extract subject
def fill_template_and_extract_subject(template_text, replacements):
    formatted = template_text.format(**replacements)
    subject_match = re.search(r'Subject\s*:\s*(.*)', formatted)
    if subject_match:
        subject = f"Follow-up – {subject_match.group(1).strip()}"
        body = re.sub(r'Subject\s*:\s*.*\n?', '', formatted, count=1).strip()
    else:
        subject = "Follow-up"
        body = formatted.strip()
    return subject, body


# Generate from predefined adaptive template (option 4)
def generate_default_phishing_email():
    print("Using adaptive phishing template.\n")

    replacements = prompt_user_replacements()
    template_path = choose_template(replacements['personal_status'], replacements['kids_info'])

    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template_text = file.read()
            return fill_template_and_extract_subject(template_text, replacements)
    except FileNotFoundError:
        print("Template not found. Using fallback.")
        return "Security Alert", "Could not load the selected template."


# Main entry point
if __name__ == "__main__":
    subject, message = load_email_pattern()

    print("\n--- PHISHING EMAIL PREVIEW ---")
    print("Subject:", subject)
    print(message)

    send = input("\nDo you want to send this email? (y/n): ").strip().lower()
    if send == 'y':
        recipient = input("Enter recipient email: ")
        attachment_path = input("Enter path to file to attach: ").strip()
        send_email(subject, message, recipient, attachment_path)
