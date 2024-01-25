from PyPDF2 import PdfReader
import re
import csv
import os

# Function to process PDF file and create a CSV
def process_pdf_file(pdf_path):
    reader = PdfReader(pdf_path)

    # Extract text from the PDF
    text = ''
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Patterns for extracting data
    phone_regex = r'\(?\b\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    general_name_regex = r'(.+?)\s\(Age:'  # General pattern for full name
    dob_regex = r'\bDOB:(\d{1,2}/\d{1,2}/\d{4})'  # Pattern for date of birth

    # Extract phone numbers and date of birth from text
    unique_phone_numbers = list(set(re.findall(phone_regex, text)))  # Remove duplicates
    date_of_birth_match = re.search(dob_regex, text)
    date_of_birth = date_of_birth_match.group(1) if date_of_birth_match else None
    
    # Use a general pattern to capture text preceding "(Age: XX)" and take the first occurrence as the full name
    general_names = [match.group(1) for match in re.finditer(general_name_regex, text)]
    full_name = general_names[0] if general_names else None

    # Prepare data for CSV
    data = {
        "Name": full_name,
        "DOB": date_of_birth,
        "Phone Numbers": unique_phone_numbers,
        "Source Name": os.path.basename(pdf_path).replace('.pdf', '')
    }

    print(f"Processing {pdf_path}")
    print("Extracted Data:", data)

    return data
