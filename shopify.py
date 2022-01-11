# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 22:57:44 2021

@author: chabv
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

transactions = pd.read_csv('shopify.csv')

transactions = transactions.iloc[:, 0:-1]

transactions['order_amount'].sum()/5000

#check for missing values, no missing values and duplicates across all 8 colmuns

missing = transactions.isna().sum()

duplicates = transactions.duplicated(keep = "first").sum()

transactions.dtypes

transactions['order_amount'].median()

# get day of the week

transactions["created_at"] = transactions["created_at"].apply(lambda i: i[:10])
transactions["created_at"] = pd.to_datetime(transactions["created_at"], format='%Y/%m/%d')

# add average price column for each transaction
transactions['price_per_sneaker'] = transactions['order_amount']/ transactions['total_items']

# check price per sneaker for each shop

store_stats = transactions.groupby("shop_id").agg({"price_per_sneaker":['mean', 'min', 'max']}) # since one sneaker all same

store_stats.columns = ["price_mean", "price_min", "price_max"]
store_stats = store_stats.reset_index()

#now can plot to see the range of prices


# zoomed out
sns.catplot(x = "shop_id",
            y = "price_mean",
            kind = "bar",
            data = store_stats)


plt.xlim(0, 100)
plt.xticks(rotation=90)
plt.show()



store_stats.describe()





transactions["day_of_week"] = transactions["created_at"].dt.day_name()



sns.catplot(x='day_of_week', 
            y='order_amount',
           kind = "bar",
             data=transactions)



# average price per a pair of sneakers
transactions['order_amount'].sum()/transactions['total_items'].sum()


#WE have an insanely high price mean

#check prder_amount by date
sns.set_style('darkgrid')
sns.lineplot(x='created_at', y='order_amount',
             markers=True,
              data=transactions)

plt.xticks(rotation=45)



# filter out transaction with abnormal average

# domain knowledge would say sneaker price should not be > 500
def check_normal_price(row: float) -> bool:
    """Check normal price.
    
    A function to check if the price of a pair of sneakers is normal
    
    :param row: a flaot
    :precondition: row is a float type
    :postcondition: checks if the price is normal (below 500)
    :return: boolean value, True if price is normal, False if abnormal 

    """
    
    return row['price_per_sneaker'] < 500
        

transactions['normal_price'] = transactions.apply(lambda price: check_normal_price(price), axis =1)



abnormal_transactions = transactions[transactions['normal_price'] == False] 



#ABNORMAL ANALYSIS

shop_ids = abnormal_transactions.groupby("shop_id")["order_id"].count()   #shop_id 78 has 46 abnormal orders


# check perhaps by payment type



#plot it



abnormal_payment_types_totals = abnormal_transactions.groupby("payment_method")["order_amount"].sum().sort_values(ascending=False).reset_index()

#plot it

sns.catplot(x = "payment_method",
            y = "order_amount",
            kind = "bar",
            data = abnormal_payment_types_totals)



#NORMAL ANALYSIS
normal_transactions = transactions[transactions['normal_price'] == True]
#metrics to use


store_stats = normal_transactions.groupby("shop_id").agg({"order_amount":['mean', 'min', 'max']}) # since one sneaker all same
store_stats.columns = ["price_mean", "price_min", "price_max"]
store_stats = store_stats.reset_index()

# zoomed out
sns.catplot(x = "shop_id",
            y = "price_mean",
            kind = "bar",
            data = store_stats)

plt.ylim(0, 10000)
plt.xlim(0, 100)
plt.xticks(rotation=90)
plt.show()


store_stats.describe()

trial = normal_transactions[normal_transactions['order_amount'] > 100000]
# AVERAGE ORDER VALUE PER DAY

aov_per_day = normal_transactions.groupby("created_at").agg({"order_amount" : ["mean"]}).reset_index()
aov_per_day.columns = ["created_at", "aov"]


sns.set_style('darkgrid')
sns.lineplot(x='created_at', y='aov',
             markers=True,
             dashes=False, data= aov_per_day)


plt.xticks(rotation=90)


#check quanityt of ordders by payment method. They are almost the same
normal_payment_types = normal_transactions.groupby("payment_method")["order_id"].count().sort_values(ascending=False).reset_index()
sns.catplot(x = "payment_method",
            y = "order_id",
            kind = "bar",
            data = normal_payment_types)



aov_per_payment_method = normal_transactions.groupby("payment_method").agg({"order_amount": ["mean", "max"]}).reset_index()
aov_per_payment_method.columns = ["payment_method", "mean", "max"]
aov_per_payment_method = aov_per_payment_method.sort_values(by = "mean")
# however, almost same when credit card is used

sns.catplot(x = "payment_method",
            y = "mean",
            kind = "bar",
            data = aov_per_payment_method)



#aov by date of the week

aov_per_day = normal_transactions.groupby("day_of_week").agg({"order_amount": ["mean", "max"]}).reset_index() 
aov_per_day.columns = ["day", "mean", "max"]
aov_per_day= aov_per_day.sort_values(by="mean")

sns.catplot(x = "day",                 # weekends have a high aov
            y = "mean",
            kind = "bar",
            data = aov_per_day)



#aov by date for whole month



normal_transactions['order_amount'].sum()/len(normal_transactions)
store_stats_two = normal_transactions.groupby("shop_id").agg({"order_amount":['mean', 'min', 'max']}).reset_index() # since one sneaker all same
store_stats_two.columns = ['shop_id', 'mean', 'min', 'max']

store_stats_two[store_stats_two['mean'] > 500]["shop_id"] # shop number 42 also skewes our average order value

shop_42 = normal_transactions[normal_transactions['shop_id'] == 42]


shop_42['order_amount'].sum()/len(shop_42)

shop_42['total_items'].max()

shop_42.groupby('total_items').count()


normal_transactions = normal_transactions[normal_transactions["shop_id"] != 42]
normal_transactions["order_amount"].sum()/len(normal_transactions)

normal_transactions["order_amount"].median()

normal_transactions["order_amount"].mode()


# since its only 2 stores shouldnt affect much







