#!/usr/bin/env python
# coding: utf-8

# ## Import Necessary Libraries

# In[1]:


import pandas as pd
import os


# ## Merge 12 months of sales data into a single CSV file

# In[15]:


path = "./SalesAnalysis/Sales_Data/"
files = os.listdir(path)

get_csv = lambda file: pd.read_csv(f"{path}{file}")
get_csvs = lambda files: map(get_csv, files)
concat_csvs = lambda files: pd.concat(get_csvs(files))

concat_csvs(files).to_csv("all_data.csv", index = False)


# ## Understand the datastructure of the CSV

# ### Read in updated dataframe

# In[16]:


all_data = pd.read_csv("all_data.csv")
all_data


# ### Print a concise summary of our dataframe

# In[17]:


all_data.info()


# ### Check the first few records

# In[18]:


all_data.head()


# ### Check the last few records

# In[19]:


all_data.tail()


# ## Clean up the data

# ### Select all rows with NaN under an entire DataFrame
# We just want to have an idea how many rows contain NaN values

# In[7]:


all_data[all_data.isna().any(axis=1)]


# ### Create a function to drop rows with NaN values

# In[8]:


drop_na = lambda df: df.dropna().reset_index(drop = True)
drop_na(all_data)


# ### Drop redundant header rows
# For some reason, the raw data contains multiple header rows and this is causing problem when we try to convert our date column
# 
# Our data header is:
# ```
# Order ID, Product, Quantity Ordered, Price Each, Order Date, Purchase Address
# ```

# #### Create a function to get indexes of header rows
# We need to know the indexes of the rows we want to drop from the dataframe

# In[9]:


get_header_row_indexes = lambda df, col: df[df[col] == col].index
get_header_row_indexes(all_data, 'Order ID')


# #### Create a function to drop rows with NaN values

# In[10]:


drop_header_rows = lambda df, col='Order ID': df.drop(get_header_row_indexes(df, col))
drop_header_rows(all_data)


# ### Create the clean data variable and call all cleaning functions
# The 2 functions we will be calling are `drop_na` and `drop_header_rows`.
# 
# We are expecting there will be `185950` rows left since there are `186850` original rows and `545` NaN values and `355` redundant header rows.
# 
# ```
# 186850 - 545 - 355 = 185950 rows
# ```

# In[11]:


def get_clean_data(df):
    return df.pipe(drop_na).pipe(drop_header_rows)
 
clean_data = get_clean_data(all_data)
clean_data


# ### Create a csv file for the clean data

# In[12]:


clean_data.to_csv("clean_data.csv", index = False)


# ## Augment data with additional columns

# ### Add Month column

# In[13]:


# Tutorial method
# all_data['Month'] = all_data['Order Date'].str[0:2]
# all_data['Month'] = all_data['Month'].astype('int32') # Need to use clean data since there are NaN values


# In[14]:


get_order_month = lambda df: pd.to_datetime(df['Order Date'], format="%m/%d/%y %H:%M").dt.strftime('%m')

# Sidenote: Need to use the clean data since there are duplicate header rows which is causing error in date conversion 
clean_data.assign(
    Month = get_order_month(clean_data)) 


# ## Questions to answer
# 
# 1. What was the best month for sales? How much was earned that month?
# 1. What city sold the most product?
# 1. What time should we display advertisemens to maximize the likelihood of customer’s buying product?
# 1. What products are most often sold together?
# 1. What product sold the most? Why do you think it sold the most?
