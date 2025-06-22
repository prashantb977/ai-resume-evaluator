import re

def extract_resume_data(text):
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    return {
        "Name": name,
        "Email": email,
        "Phone": phone
    }

def extract_name(text):
    lines = text.strip().split('\n')
    if lines:
        return lines[0].strip().title()
    return "Not Found"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not Found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\-\(\) ]{8,}\d', text)
    return match.group(0) if match else "Not Found"
