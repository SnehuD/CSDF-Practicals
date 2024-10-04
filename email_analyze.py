import email
from email import policy
from email.parser import BytesParser

def parse_email_header(file_path):
    # Read the email content from the file
    with open(file_path, 'rb') as file:
        msg = BytesParser(policy=policy.default).parse(file)
    
    # Extract header details
    from_ = msg['From']
    to = msg['To']
    subject = msg['Subject']
    date = msg['Date']
    message_id = msg['Message-ID']

    # Print the extracted information
    print(f"From: {from_}")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Date: {date}")
    print(f"Message-ID: {message_id}")

if __name__ == "__main__":
    # Use a raw string or forward slashes to avoid unicode errors
    #parse_email_header(r"C:\Users\rayra\Downloads\Final Alert _ Solve & grab the Samsung flagship mobile _ Samsung Galaxy AI Treasure Hunt.eml")
    # Or
    parse_email_header("C:/Users/rayra/Desktop/God_Codes/PY_programs/CyberSec/IPO alert_ Dee Development _ Open to apply.eml")
