#!/usr/bin/env python
# coding: utf-8

# In[38]:


import raw_utils as util
import os

import pandas as pd
import numpy as np

import random


# ## Phishing

# ### Nazario Phishing Corpus

# We will start with reading the subset of the Phishing Corpus that we want.

# In[39]:


# Paths
nazario_path = r'E:\University of Warwick\Dissertation\Dataset\nazario'



# In[40]:


# Files to be ignored for read_dataset()
files_ignored = ['Extracted data']
files_ignored_recent = ['Extracted data', '20051114.mbox',  'phishing0.mbox',  'phishing1.mbox',  'phishing2.mbox',  'phishing3.mbox', 'private-phishing4.mbox']


# First, we will read and convert all of the dataset. It is straightforward since it is a collection of .mbox files

# In[42]:


phishing = util.read_dataset(nazario_path, files_ignored, text_only=True)


# In[43]:


phishing.info()


# In[23]:

import quopri
import base64

def combined_decode(s):
    try:
        # Check for UTF-8 Base64 encoding
        if s.startswith("=?UTF-8?B?") and s.endswith("?="):
            s = s[10:-2]
            # Check if padding is required and add if necessary
            missing_padding = len(s) % 4
            if missing_padding:
                s += '=' * (4 - missing_padding)
            return base64.b64decode(s).decode('utf-8')
        
        # Check for UTF-8 Quoted-Printable encoding
        elif s.startswith("=?UTF-8?Q?") and s.endswith("?="):
            return quopri.decodestring(s[10:-2].encode()).decode('utf-8')
        
        # If no known encoding pattern is detected, return the original string
        else:
            return s
    except Exception as e:
        # Return the original string if decoding fails
        return s
    
for i in range(phishing.shape[0]):  # iterating through rows
    for j in range(phishing.shape[1]):  # iterating through columns
        phishing.iloc[i, j] = combined_decode(str(phishing.iloc[i, j]))

# This will modify the 'phishing' DataFrame in-place.


# Export the DataFrame to a XLSX file
phishing.to_excel(r'E:\University of Warwick\Dissertation\Dataset\nazario\Extracted data\nazario_full.xlsx', index=False)



# Then, we will also take the subset of only the recent emails.

# In[7]:


phishing_recent = util.read_dataset(nazario_path, files_ignored_recent, text_only=True)


# In[8]:


phishing_recent.info()


# In[9]:


for i in range(phishing_recent.shape[0]):  # iterating through rows
    for j in range(phishing_recent.shape[1]):  # iterating through columns
        phishing_recent.iloc[i, j] = combined_decode(str(phishing_recent.iloc[i, j]))


# Export the DataFrame to a XLSX file
phishing_recent.to_excel(r'E:\University of Warwick\Dissertation\Dataset\nazario\Extracted data\nazario_recent.xlsx', index=False)


# ## Legitimate

# ### Enron Email Dataset

# This dataset is very big in size so we will just sample different sized sets of random emails from it.

# In[10]:


filename = util.sample_enron_to_mbox(enron_path, 2000)
enron_2000 = util.mbox_to_df(filename, enron_path+'/mbox', text_only=True)
util.save_to_csv(enron_2000, csv_path, 'enron_text_2000.csv')


# In[11]:


filename = util.sample_enron_to_mbox(enron_path, 20000)
enron_20000 = util.mbox_to_df(filename, enron_path+'/mbox', text_only=True)
util.save_to_csv(enron_20000, csv_path, 'enron_text_20000.csv')

