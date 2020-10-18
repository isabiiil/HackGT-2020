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
import datetime
import time
import altair as alt
from sklearn.linear_model import LinearRegression



st.title('HackGT')
st.title("Info by Touch Point ID")
#load json object
print("###################################### NEW LINE ========================")
with open('tlogInfo.json') as f:
    d = json.load(f)
df = pd.json_normalize(d['tlogs'])



# =========== Discount amounts at various touch point locations ==========
st.header("Discount Ammount Line Plot")
touch_point_id_options = df['touchPointId'].unique()
touch_point_id = st.sidebar.selectbox(
  'Which touchpoint ID would you like to see?',
  touch_point_id_options
)

touch_point_query_df = df[(df['touchPointId'] == touch_point_id)]
#=====================================================================
#Discount Amount timeline
y = touch_point_query_df['tlog.totals.discountAmount.amount']

x = touch_point_query_df['openDateTimeUtc.dateTime']

time = [ datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ') for date in x.values ]

linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(np.array([int(date.strftime('%Y%m%d')) for date in time]).reshape(-1,1), y)  # perform linear regression
Y_pred = linear_regressor.predict(np.array([int(date.strftime('%Y%m%d')) for date in time]).reshape(-1,1))
print(Y_pred)
# print(time)
data = pd.DataFrame({
  'date': time,
  'Discount Ammount $': y.values
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.line_chart(data)

# #============================================================
# #Spending Amount timeline
st.header("Grand Ammount Line Plot")
y = touch_point_query_df['tlog.totals.grandAmount.amount']
data = pd.DataFrame({
  'date': time,
  'Grand Ammount $': y.values
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.line_chart(data) 



# #====================================================================
#Productwise Sale at a particular Point of Contact
df_prod = pd.io.json.json_normalize(np.hstack(touch_point_query_df['tlog.items']))
# print(df_prod['productName'].values)
# fig, ax = plt.subplots()
# ax.hist(df_prod['productName'].values, bins = len(df_prod['productName'].values))
# print(dir(ax))
# st.pyplot(fig)
# print(df_prod['productName'].value_counts())
st.header("Items Popularity at a Touchpoint ID")
features = np.array(['feature 1', 'feature 2', 'feature 3'])
features_importances = np.array([.5, .25, .4])
products = df_prod['productName']
# print(np.array(df.value_counts().index))
chart_data = pd.DataFrame()
chart_data['Items'] = np.array(products.value_counts().index)
chart_data['Frequency'] = np.array(df_prod['productName'].value_counts().values)

chart_v1 = alt.Chart(chart_data).mark_bar().encode(
x='Items',
y='Frequency')
st.write("", "", chart_v1)



# #Querying the location ID 
# #===================================================================
# location_id = input("Enter the location id: ") 
# print(location_id)

st.title("Info by Location ID")
st.header("Discount Ammount Line Plot")
# sidebar for Location ID
location_id_options = df['tlog.location.locationId'].unique()
location_id = st.sidebar.selectbox(
  'Which Location ID would you like to see?',
  location_id_options
)

location_query_df = df[(df['tlog.location.locationId'] == location_id)]
# print(location_query_df.head())
# print(location_query_df.columns)
# #=====================================================================
# #Discount Amount timeline
y = location_query_df['tlog.totals.discountAmount.amount']
x = (location_query_df['openDateTimeUtc.dateTime'])
time = [ datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ') for date in x.values ]

data = pd.DataFrame({
  'date': time,
  'Discount Ammount $': y.values
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.line_chart(data)

# #============================================================
# #Spending Amount timeline
st.header("Grand Ammount Line Plot")
y = location_query_df['tlog.totals.grandAmount.amount']
data = pd.DataFrame({
  'date': time,
  'Grand Ammount $': y.values
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.line_chart(data) 


# #============================================================
# #Productwise Sale at a particular location
df_prod = pd.io.json.json_normalize(np.hstack(location_query_df['tlog.items']))
# print(df_prod['productName'])
# fig, ax = plt.subplots()
# x = df_prod['productName']
# x.value_counts().plot(ax=ax, kind='bar')
# plt.show()
st.header("Items Popularity at a Location ID")
features = np.array(['feature 1', 'feature 2', 'feature 3'])
features_importances = np.array([.5, .25, .4])
products = df_prod['productName']
# print(np.array(df.value_counts().index))
chart_data = pd.DataFrame()
chart_data['Items'] = np.array(products.value_counts().index)
chart_data['Frequency'] = np.array(df_prod['productName'].value_counts().values)

chart_v1 = alt.Chart(chart_data).mark_bar().encode(
x='Items',
y='Frequency')
st.write("", "", chart_v1)