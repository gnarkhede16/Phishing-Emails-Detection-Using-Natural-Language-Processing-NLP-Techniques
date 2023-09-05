import pandas as pd # for data munging, it contains manipulation tools designed to make data analysis fast and easy
import re # Regular Expressions - useful for extracting information from text 
import email
from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')
# For viz


enron_df = pd.read_csv(r"E:\University of Warwick\Dissertation\Dataset\Enron\Enron email dataset.csv")

# create list of email objects
emails = list(map(email.parser.Parser().parsestr,enron_df['message']))

# extract headings such as subject, from, to etc..
headings  = emails[0].keys()

# Goes through each email and grabs info for each key
# doc['From'] grabs who sent email in all emails
for key in headings:
    enron_df[key] = [doc[key] for doc in emails]
    
    
# enron_df.head()

# Useful functions
def get_raw_text(emails):
    email_text = []
    for email in emails.walk():
        if email.get_content_type() == 'text/plain':
            email_text.append(email.get_payload())
    return ''.join(email_text)

enron_df['body'] = list(map(get_raw_text, emails))

enron_df.dtypes



enron_df_new = pd.DataFrame()

enron_df_new['subject'] = enron_df['Subject']
enron_df_new['body'] = enron_df['body']


# Export the DataFrame to a XLSX file
enron_df_new.to_excel(r'E:\University of Warwick\Dissertation\Dataset\Enron\Extracted data\enron_data.xlsx', index=False)




