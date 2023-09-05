import re
import email.header
import email
import pandas as pd
from bs4 import BeautifulSoup


filename = r"E:\University of Warwick\Dissertation\Dataset\Cambridge\year2015.txt"


with open(filename, "r", encoding='utf-8') as file:
    text = file.read()
    
    

def decode_html_content(html_content):
    '''Extracts text from HTML content using BeautifulSoup.'''
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n').strip()

def extract_body_and_subject_from_email(email_str):
    # Extract subject
    subject_match = re.search(r'Subject: (.+)', email_str)
    subject = subject_match.group(1) if subject_match else "No Subject Found"
    
    # Extract body
    b = email.message_from_string(email_str)
    body = ""

    def decode_payload(payload):
        try:
            decoded_str = payload.decode('utf-8')
        except UnicodeDecodeError:
            try:
                decoded_str = payload.decode('ISO-8859-1')
            except:
                decoded_str = payload.decode('utf-8', errors='replace')  # replace problematic characters
        return decode_html_content(decoded_str)

    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
                body = decode_payload(body)
                break
            elif ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
                body = decode_payload(body)
                break
    else:
        body = b.get_payload(decode=True)
        body = decode_payload(body)

    return [subject, body]



# Split the text by the "From <>" pattern to separate individual emails
emails = re.split(r'From <>', text)[1:]  # The first item is empty or unrelated text, so we skip it

# Extract the body from each email
extracted_text = [extract_body_and_subject_from_email(e) for e in emails if e]

print(extracted_text)



# Convert the extracted data to a DataFrame
df = pd.DataFrame(extracted_text, columns=["Subject", "Body"])

# Export the DataFrame to a CSV file
df.to_excel(r"E:\University of Warwick\Dissertation\Dataset\Cambridge\Extracted data\data2011.xlsx", index=False)


    


# extract headings such as subject, from, to etc..
headings  = emails[0].keys()

# Goes through each email and grabs info for each key
# doc['From'] grabs who sent email in all emails
for key in headings:
    df[key] = [doc[key] for doc in emails]












