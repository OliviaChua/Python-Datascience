#!/usr/bin/env python
# coding: utf-8

# ## Import Necessary Libraries

# In[1]:


import pandas as pd
import os


# ## Merge 12 months of sales data into a single CSV file

# In[2]:


files = [file for file in os.listdir("./SalesAnalysis/Sales_Data/")]

get_csv = lambda file: pd.read_csv(f"./SalesAnalysis/Sales_Data/{file}")
get_csvs = lambda files: (*map(get_csv, files),)
concat_csvs = lambda files: pd.concat(get_csvs(files))

concat_csvs(files).to_csv("all_data.csv", index = False)


# ## Understand the datastructure of the CSV

# ### Read in updated dataframe

# In[6]:


all_data = pd.read_csv("all_data.csv")


# ### Print a concise summary of our dataframe

# In[7]:


all_data.info()


# ### Check the first few records

# In[8]:


all_data.head()


# ### Check the last few records

# In[9]:


all_data.tail()

