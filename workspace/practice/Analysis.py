#!/usr/bin/env python
# coding: utf-8

# ## Import Necessary Libraries

# In[1]:


import pandas as pd
import os


# ## Merge 12 months of sales data into a single CSV file

# In[2]:


path = "../data/Sales_Data/"
output_path = "../output/"
files = os.listdir(path)

get_csv = lambda file: pd.read_csv(f"{path}{file}")
get_csvs = lambda files: map(get_csv, files)
concat_csvs = lambda files: pd.concat(get_csvs(files))

concat_csvs(files).to_csv(f"{output_path}all_data.csv", index = False)


# ## Understand the datastructure of the CSV

# ### Read in updated dataframe

# In[3]:


all_data = pd.read_csv(f"{output_path}all_data.csv")
all_data


# ### Print a concise summary of our dataframe

# In[4]:


all_data.info()


# ### Check the first few records

# In[5]:


all_data.head()


# ### Check the last few records

# In[6]:


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
    return (df
            .pipe(drop_na)
            .pipe(drop_header_rows)
            .assign(
                    # Convert Order Date from str to date format
                    **{'Order Date': lambda df_: pd.to_datetime(df_['Order Date'], format="%m/%d/%y %H:%M")},
                    # Convert Quantity Ordered and Price Each to numeric
                    **{'Quantity Ordered': lambda df_: pd.to_numeric(df_['Quantity Ordered'])},
                    **{'Price Each': lambda df_: pd.to_numeric(df_['Price Each'])})
           )
 
clean_data = get_clean_data(all_data)
clean_data


# ### Create a csv file for the clean data

# In[12]:


clean_data.to_csv(f"{output_path}clean_data.csv", index = False)


# ## Augment data with additional columns

# ### Add Month column

# In[13]:


get_order_month = lambda df: df['Order Date'].dt.month


# ### Add Date column

# In[14]:


get_order_date = lambda df: df['Order Date'].dt.date


# ### Add Hour column

# In[15]:


get_order_hour = lambda df: df['Order Date'].dt.hour


# ### Add Minute column

# In[16]:


get_order_minute = lambda df: df['Order Date'].dt.minute


# ### Add Sales column

# In[17]:


get_sales = lambda df: df['Quantity Ordered'] * df['Price Each']


# ### Add City column

# In[18]:


get_cities = lambda df: df['Purchase Address'].str.extract(r'((?<=,\s).*?(?=,))')


# ### Add State column

# In[19]:


get_states = lambda df: df['Purchase Address'].str.extract(r'((?<=,\s)[A-z]{2}(?=\s\d))')


# ### Create final data variable and call all augmenting functions
# 
# We will be using `clean_data` and not the original data `all_data` due to the following reason:
# 
# 1. There are NaNs in the original data which can affect the result of the analysis
# 2. There are duplicate header rows which is causing error in the date conversion `to_datetime` which is part of the `get_order_month` function
# 3. There are some incorrect data types for some columns
#  - The `Order Date` needs to be in date format so it is easier to get the month, day, year, or time from this column
#  - The `Quantity Ordered` and `Price Each` columns need to be numeric in order for the `get_sales` function to work

# In[20]:


final_data = clean_data.assign(
    Month = get_order_month(clean_data),
    Date = get_order_date(clean_data),
    Hour = get_order_hour(clean_data),
    Minute = get_order_minute(clean_data),
    Sales = get_sales(clean_data),
    City = get_cities(clean_data) + ' (' + get_states(clean_data) + ')',
    ) 
final_data


# ## Questions to answer
# 
# 1. What was the best month for sales? How much was earned that month?
# 2. What specific date earned the most sales?
# 3. What city sold the most product?
# 4. What time should we display advertisemens to maximize the likelihood of customer’s buying product?
# 5. What products are most often sold together?
# 6. What product sold the most? Why do you think it sold the most?

# ### What was the best month for sales? How much was earned that month?

# In[21]:


# Generic function
get_grouped_sum = lambda df, groupby_col: (
    (df
     .groupby(groupby_col)
     .sum()
    )
)

sales_month_results = get_grouped_sum(final_data, 'Month')
sales_month_results.sort_values('Sales')


# In[22]:


import matplotlib.pyplot as plt

# Generic function
get_x_data = lambda df, col: [x for x, y in df.groupby(col)]

months = get_x_data(final_data, 'Month')

plt.bar(months, sales_month_results['Sales'])
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month')


# ### What specific date earned the most sales?

# In[23]:


get_grouped_sum(final_data, 'Date').sort_values('Sales')


# In[24]:


import datetime
final_data[final_data['Date'] == datetime.date(2019,12,4)]['Sales'].sum()


# ### What city sold the most product?

# In[25]:


sales_city_results = get_grouped_sum(final_data, 'City')
sales_city_results.sort_values('Sales')


# In[26]:


cities = get_x_data(final_data, 'City')

plt.bar(cities, sales_city_results['Sales'])
plt.xticks(rotation = 'vertical', size = 8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City')


# ### What time should we display advertisemens to maximize the likelihood of customer’s buying product?
# 
# Based on the chart below, we have peaks at 11 am, 12pm and 7 pm. 
# 
# Good times to display ads:
# 
# - 10 am to 12 pm
# - 6 pm to 7 pm

# In[27]:


hours = get_x_data(final_data, 'Hour')

# Count the number of rows by the hour
plt.plot(hours, final_data.groupby('Hour').count())
plt.xticks(hours)
plt.grid()
plt.ylabel('Number of Orders')
plt.xlabel('Hours')


# ### What products are most often sold together?

# In[28]:


get_duplicate_records = lambda df, col: df[df.duplicated(subset = [col],keep = False)]

add_grouped_prod_col = lambda df, groupby_col: df.assign(Grouped = df.groupby(groupby_col)['Product'].transform(lambda x: ','.join(x)))


get_grouped_prod = lambda: (
    final_data
    .pipe(get_duplicate_records, col = 'Order ID')
    .pipe(add_grouped_prod_col, groupby_col = 'Order ID')
    .loc[:, ['Order ID', 'Grouped']]
    .drop_duplicates()
    .assign(Group = lambda df_: df_['Grouped'].str.split(",").str.len())
)

get_grouped_prod()


# In[29]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in get_grouped_prod()['Grouped']:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list, 2)))
    
for key, val in count.most_common(10):
    print(key, val)


# The method below only gives an estimate count

# In[30]:


get_grouped_prod().value_counts(subset=['Grouped','Group'], sort = True)


# ### What product sold the most? Why do you think it sold the most?

# In[31]:


quantity_product_results = get_grouped_sum(final_data, 'Product')
quantity_product_results.sort_values('Quantity Ordered')


# In[32]:


products = get_x_data(final_data, 'Product')
quantity_ordered = quantity_product_results['Quantity Ordered']

plt.bar(products, quantity_ordered)
plt.xticks(rotation = 'vertical', size = 8)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')


# In[33]:


prices = final_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax1.set_xticklabels(products, rotation='vertical', size=8)
ax2.set_ylabel('Price ($)', color='b')

fig.show()

