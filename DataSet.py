#!/usr/bin/python3
 
import os
import csv
import pandas as pd
import email
import email.policy
import email.parser
from bs4 import BeautifulSoup

header = ['mail', 'body', 'label']
data = []

## Found here : https://www.kaggle.com/code/veleon/spam-classification/notebook 
ham_list = [name for name in sorted(os.listdir('Data/ham')) if len(name) > 20]
spam_list = [name for name in sorted(os.listdir('Data/spam')) if len(name) > 20]

def load_email(is_spam, filename):
    directory = "Data/spam" if is_spam else "Data/ham"
    with open(os.path.join(directory, filename), "rb") as f:
        return email.parser.BytesParser(policy=email.policy.default).parse(f)
    
ham_emails = [load_email(is_spam=False, filename=name) for name in ham_list]
spam_emails = [load_email(is_spam=True, filename=name) for name in spam_list]

def html_to_plain(email):
    try:
        soup = BeautifulSoup(email.get_content(), 'html.parser')
        return soup.text.replace('\n\n','')
    except:
        return ""

def email_to_plain(email):
    for part in email.walk():
        partContentType = part.get_content_type()
        if partContentType not in ['text/plain','text/html']:
            continue
        try:
            partContent = part.get_content()
        except:
            partContent = str(part.get_payload())
        if partContentType == 'text/plain':
            return partContent
        else:
            return html_to_plain(part)

## End of sourced code

with open('spamham.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for spam in spam_emails:
      try:
        simplest = email_to_plain(spam)
        writer.writerow([spam['from'], simplest, 'spam'])
      except:
          pass

    for ham in ham_emails:
      try:
        simplest = email_to_plain(ham)
        writer.writerow([ham['from'], simplest, 'ham'])
      except:
          pass

    df = pd.read_csv('spamham.csv') # avoid header=None. 
    shuffled_df = df.sample(frac=1)
    shuffled_df.to_csv('shuffled_spamham.csv', index=False)