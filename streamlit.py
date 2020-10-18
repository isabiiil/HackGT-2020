import streamlit as st
import numpy as np
import pandas as pd
import time
import json 
from pandas.io.json import json_normalize #package for flattening json in pandas df
import matplotlib.pyplot as plt
import dateutil.parser
from PIL import Image
from PIL import ImageOps
import gc

st.title('HackGT')

#load json object
with open('tlogInfo.json') as f:
    d = json.load(f)
df = pd.json_normalize(d['tlogs'])

#Querying the touch_point ID
#===================================================================
touch_point_id = st.sidebar.selectbox(
  'Which touchpoint ID would you like to see?',
  ('1', '2', '3', '4', '5', )
)

touch_point_query_df = df[(df['touchPointId'] == touch_point_id)]
#=====================================================================
#Discount Amount timeline
y = touch_point_query_df['tlog.totals.discountAmount.amount']
x = touch_point_query_df['openDateTimeUtc.dateTime']
discount = pd.DataFrame(y, x)
st.line_chart(touch_point_query_df)
st.line_chart(discount)
# plt.ylabel('Discount Amount ($)')
# plt.xlabel('Time')

# fig1 = plt.figure(1)
# scatter = plt.plot(x, y, marker = 'o', alpha = 0.8)
# plt.show()
# plt.cla()
# plt.close()
#============================================================
#Spending Amount timeline
y = touch_point_query_df['tlog.totals.grandAmount.amount']
x = (touch_point_query_df['openDateTimeUtc.dateTime'])
plt.ylabel('Spending Amount ($)')
plt.xlabel('Time')
fig1 = plt.figure(1)
scatter = plt.plot(x, y, marker = 'o', alpha = 0.8)
plt.show()
plt.cla()
plt.close()
#====================================================================
#Productwise Sale at a particular Point of Contact
df_prod = pd.io.json.json_normalize(np.hstack(touch_point_query_df['tlog.items']))
print(df_prod['productName'])
fig, ax = plt.subplots()
x = df_prod['productName']
x.value_counts().plot(ax=ax, kind='bar')
plt.show()


#Querying the location ID 
#===================================================================
location_id = input("Enter the location id: ") 
print(location_id)
location_query_df = df[(df['tlog.location.locationId'] == location_id)]
print(location_query_df.head())
print(location_query_df.columns)
#=====================================================================
#Discount Amount timeline
y = location_query_df['tlog.totals.discountAmount.amount']
x = (location_query_df['openDateTimeUtc.dateTime'])
plt.ylabel('Discount Amount ($)')
plt.xlabel('Time')
fig1 = plt.figure(1)
scatter = plt.plot(x, y, marker = 'o', alpha = 0.8)
plt.show()
plt.cla()
plt.close()
#============================================================
#Spending Amount timeline
y = location_query_df['tlog.totals.grandAmount.amount']
x = (location_query_df['openDateTimeUtc.dateTime'])
plt.ylabel('Spending Amount ($)')
plt.xlabel('Time')

fig1 = plt.figure(1)
scatter = plt.plot(x, y, marker = 'o', alpha = 0.8)
plt.show()
plt.cla()
plt.close()

#============================================================
#Productwise Sale at a particular location
df_prod = pd.io.json.json_normalize(np.hstack(location_query_df['tlog.items']))
print(df_prod['productName'])
fig, ax = plt.subplots()
x = df_prod['productName']
x.value_counts().plot(ax=ax, kind='bar')
plt.show()