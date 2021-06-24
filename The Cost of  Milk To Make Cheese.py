#!/usr/bin/env python
# coding: utf-8

# ## The cost of milk to make cheese
# <p>The Coronavirus outbreak has caused major economic disruption. The pandemic's impact on the tourism, travel, and hospitality industries has featured frequently in 2020 news reports, but the economic impact has not been isolated to these industries alone. </p>
# <p>The UK dairy industry is one such affected industry and has had to work together to address current market challenges and avoid milk waste. The industry can adapt to the temporary decrease in demand by identifying opportunities for processing the milk into storable products such as butter, cheese, and skimmed milk powder. </p>
# <p>The UK Department of Environment, Food, and Rural Affairs has contracted your company to perform a detailed analysis of the UK dairy industry to help them understand the industry's value. </p>
# <p>Your team has divided the analysis project into several tasks. One of the tasks is to determine the value of the cheddar cheese industry. The revenue from cheese is much more than, for example, whole milk, but a kilogram of cheese requires almost ten liters of raw milk to make. Your first task is to determine the annual cost of milk needed to produce cheddar cheese over the past five years. </p>
# <p>You have been provided with three datasets. <em><strong>Please note that 1000 kg = 1 metric tonne.</strong></em></p>
# <div style="background-color: #efebe4; color: #05192d; text-align:left; vertical-align: middle; padding: 15px 25px 15px 25px; line-height: 1.6;">
#     <div style="font-size:16px"><b>datasets/milk_prices.csv - The monthly prices, volume, protein percentage and butterfat percentage of milk </b>
#     </div>
# Source: <a href="https://environment.data.gov.uk/linked-data/cube/explore?uri=http%3A%2F%2Fenvironment.data.gov.uk%2Flinked-data%2Fcatalog%2Fdatasets%2Fentry%2Fmilk-prices-and-composition-of-milk-annual-statistics&filters-drawer=closed">Defra Data Services Platform</a>
# <ul>
#     <li><b>Time: </b>The month and year when the value was recorded.</li>
#     <li><b>Measure Type: </b>The type of measure recorded.</li>
#     <li><b>Price:</b> The price of milk (in Pounds per liter).</li>
#     <li><b>Volume:</b> The amount of milk produced (in million liters).</li>
#     <li><b>Protein:</b> The protein content of the milk (percentage).</li>
#     <li><b>Butterfat:</b> The butterfat content of the milk (percentage).</li>
#     <li><b>Unit of Measure:</b> The units specific to the measure type.</li>
# </ul>
# </div>
# <div style="background-color: #efebe4; color: #05192d; text-align:left; vertical-align: middle; padding: 15px 25px 15px 25px; line-height: 1.6; margin-top: 17px;">
#     <div style="font-size:16px"><b>datasets/Milk_products_production.csv - The monthly production figures of milk, cream and cheddar cheese</b>
#     </div>
# Source: <a href="https://www.gov.uk/government/statistics/milk-utilisation-by-dairies-in-england-and-wales">GOV.UK</a>
#     <ul>
#         <li><b>Unnamed: 0: </b>The year and month when the value was recorded.</li>
#         <li><b>Liquid Milk Production: </b>The total amount of milk produced (in million liters).</li>
#         <li><b>Cream Production: </b>The total amount of cream produced (in million liters).</li>
#         <li><b>Cheddar Cheese Production:</b>The total amount of cheddar cheese produced (in thousand tonnes).</li>
#     </ul>
# </div>
# <div style="background-color: #efebe4; color: #05192d; text-align:left; vertical-align: middle; padding: 15px 25px 15px 25px; line-height: 1.6; margin-top: 17px;">    
#     <div style="font-size:16px"><b>datasets/conversion_factors.xls - Liters of milk used to make one kilogram of product</b>
#     </div>
# Source: <a href="https://www.gov.uk/government/statistics/milk-utilisation-by-dairies-in-england-and-wales">GOV.UK</a>
#     <ul>
#         <li><b>Product: </b>The type of product.</li>
#         <li><b>Conversion factor (litres/kg):</b> Liters of milk used to make one kilogram of product (in liters/kg).</li>
#     </ul>
# </div>

# In[2]:


get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[52]:


#importing necessary packages

import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
import datetime as dt

#reading first dataset
raw_milk = pd.read_csv('datasets/milk_prices.csv')

#renaming columns
cols = ['Date', 'Measure type', 'Price', 'Volume', 'Protein', 'Butterfat',
       'Unit of Measure']
raw_milk.columns = cols


# In[53]:


#conversion and extracting datetime data
raw_milk['month'] = pd.to_datetime(raw_milk['Date'], format='%Y-%m').dt.month
raw_milk['year'] = pd.to_datetime(raw_milk['Date'], format='%Y-%m').dt.year

#inspecting dataframe
display(raw_milk.head(10))
raw_milk.info()


# In[54]:


#notice that the "Measure Type" column combine 4 distinct values (price, volume, protein, butterfat)
raw_milk['Measure type'].unique()


# In[55]:


#we are only interested in Price
raw_milk = raw_milk[raw_milk['Measure type'] == 'Price']

#checking NA values for dataframe column we're interested in
raw_milk.Price.isna().sum()
#hence we can drop the column "Measure type" and focus on "Price" column


# In[63]:


#grouping Price column by month and year where year is past 5 years
raw_milk = raw_milk[raw_milk.year > 2014]
raw_milk_price = raw_milk.groupby(['year','month'])[['Price']].sum().reset_index()

raw_milk_price.head()


# In[66]:


#importing 2nd dataset
milk_production = pd.read_csv('datasets/Milk_products_production.csv')
col_production = ['Date', 'liquid_milk_production', 'cream_production',
       'cheddar_cheese_production']
milk_production.columns = col_production

milk_production.head()

#take note theres a unit on the first row
#notice the units are with comma and possibly string type


# In[67]:


#drop first row
milk_production.drop([0], inplace=True)

#conversion to datetime format
milk_production['year'] = pd.to_datetime(milk_production['Date'], format="%b-%y").dt.year
milk_production['month'] = pd.to_datetime(milk_production['Date'], format="%b-%d").dt.month

#remove non relevant columns
milk_production.drop(['liquid_milk_production','cream_production','Date'], axis=1, inplace=True)


#convert data type for relevant column
milk_production.cheddar_cheese_production = milk_production.cheddar_cheese_production.str.replace(',','.').astype('float64')
display(milk_production.info())
milk_production.head()


# In[50]:


milk_production.year.unique()


# In[70]:


#merge 1st and 2nd dataframe on month and year
merged = pd.merge(raw_milk_price, milk_production, on=['year', 'month'])
merged.head()


# In[100]:


convert = pd.read_csv('datasets/conversion_factors.csv')
convert


# In[102]:


#notice in the conversion factor table above, we need 9.5 litre of milk for each 1kg cheese

#remember that the unit for Price is Pound/Litre

#remember that the unit for cheddar_cheese_production is thousand tonnes

#Cost = production * price * 1000 * 1000 * 9.5
merged['cost'] = merged.Price * merged.cheddar_cheese_production * 1000 * 1000 * 9.5
merged.head()


# In[125]:


#groupby year, aggregation type is sum
annual_milk_cost = merged.groupby('year')['cost'].sum()
annual_milk_cost


# In[137]:


for x,y in annual_milk_cost.iteritems():
    #print("The cost of milk for the year ", annual_milk_cost.index[x], "is ", annual_milk_cost.iloc[x,1])
    s = str(int(y))
    print("The cost of milk for the year", x, "is", "£"+s)

