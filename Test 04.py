#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re
import warnings

warnings.filterwarnings('ignore')

# In[2]:


df = pd.read_csv('Python Scripts\Dummy_Dataset.csv')
df.head()

# In[3]:


df.shape

# ## Check Duplicates

# In[4]:


df.duplicated().sum()

# In[5]:


dup1 = []
for i, j in zip(df.duplicated().values, df.duplicated().index.values):
    if i:
        dup1.append(j)

# In[6]:


dup1

# In[7]:


df_dup1 = df.loc[dup1]
df_dup1

# ## Remove Special Character

# In[8]:


for i, j in zip(df['Account Name'].values, df['Account Name'].index):
    x = re.sub('[^a-z0-9A-Z ]', '', str(i))
    df['Account Name'][j] = re.sub('\s+', ' ', x)

# ## Check Email Format

# In[9]:


email_indexes = []
indexes = []
for i, j in zip(df['Email'].values, df['Email'].index):
    if type(i) == str:
        # i=str.lower(i)
        x = re.findall(r'[a-zA-Z0-9_+.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', i)
        # x = re.findall(r"[a-zA-Z][a-zA-Z0-9]*[_.-]?[a-zA-Z0-9]+@[a-zA-Z]+\.com", i)
        if (x):
            indexes.append(j)
        else:
            email_indexes.append(j)

# In[ ]:


# In[10]:


df_emails = df.iloc[email_indexes]
df_emails

# In[11]:


df.iloc[indexes].head(7)

# ## Check Mobile Number Format

# In[12]:


for i in range(len(df)):
    x = re.sub("[^0-9]", "", df['Phone'][i])
    if len(x) == 10:
        if df['Country'].values[i] == 'USA':
            regex = re.compile(r"([\d]{3})([\d]{3})([\d]{4})")
            df['Phone'][i] = re.sub(regex, r"+1 (\1) \2-\3", x)

        elif df['Country'].values[i] == 'France':
            regex = re.compile(r"([\d]{3})([\d]{3})([\d]{4})")
            df['Phone'][i] = re.sub(regex, r"+33 (\1) \2-\3", x)

        elif df['Country'].values[i] == 'India':
            regex = re.compile(r"([\d]{3})([\d]{3})([\d]{4})")
            df['Phone'][i] = re.sub(regex, r"+91 (\1) \2-\3", x)

        elif df['Country'].values[i] == 'UK':
            regex = re.compile(r"([\d]{3})([\d]{3})([\d]{4})")
            df['Phone'][i] = re.sub(regex, r"+44 (\1) \2-\3", x)

# ## Remove Null Values

# In[13]:


nulls = []
for val, ind in zip(df.isna().sum().values, df.isna().sum().index):
    if val > 1:
        for i, j in zip(df.isna()[ind].values, df.isna()[ind].index):
            if i:
                nulls.append(j)

null_df = df.iloc[list(set(nulls))]
null_df

# ## good and bad dataset

# In[14]:


data_copy = pd.concat([df_dup1, df_emails, null_df], ignore_index=False)
data_copy

# In[15]:


df = df.loc[indexes]
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# In[16]:


df.shape

# ## Check Date Format

# In[17]:


for i, j in zip(df['Date'].values, df['Date'].index):
    df['Date'][j] = re.sub("[^0-9]", "/", str(i))

# In[18]:


df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df.head(3)

# ## Identify Test Data

# In[19]:


test_indexes = []
indexes = []
for i, j in zip(df['Account Name'].values, df['Account Name'].index):
    if type(i) == str:
        i = str.lower(i)
        x = re.findall(r'demo|test|sample', i)
        if (x):
            test_indexes.append(j)
        else:
            indexes.append(j)

# ## Check Dublicates

# In[21]:


df.duplicated().sum()

# In[22]:


dup2 = []
for i, j in zip(df.duplicated().values, df.duplicated().index.values):
    if i:
        dup2.append(j)
        indexes.remove(j)

# In[23]:


df_dup2 = df.loc[dup2]
df_dup2

# In[24]:


data_copy = pd.concat([data_copy, df_dup2])

# In[25]:


df.drop_duplicates(inplace=True)

# In[26]:


test_df = df.loc[test_indexes]
test_df.shape

# In[27]:


main_df = df.loc[indexes]
main_df.shape

# In[28]:


test_df.to_csv("Python Scripts\df_test.csv", index=False)
main_df.to_csv("Python Scripts\df_main.csv", index=False)
data_copy.to_csv("Python Scripts\df_bad.csv", index=False)

# In[ ]:
