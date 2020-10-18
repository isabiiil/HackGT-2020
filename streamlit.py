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
import pytz



st.title('PreDemo (Prediction Demographics)')
'\n'
st.title("Infographics for given Touch Point ID") 
#load json object
print("###################################### NEW LINE ========================")
with open('tlogInfo2.json') as f:
    d = json.load(f)
df = pd.json_normalize(d['tlogs'])



# =========== Discount amounts at various touch point locations ==========

touch_point_id_options = df['touchPointId'].unique()
touch_point_id = st.sidebar.selectbox(
  'Which touchpoint ID would you like to see?',
  touch_point_id_options
)
###############
# setting up columns
# >>> col1, col2, col3 = st.beta_columns(3)
# >>>
# >>> with col1:
# ...    st.header("A cat")
# ...    st.image("https://static.streamlit.io/examples/cat.jpg", use_column_width=True)
# ...
# >>> with col2:
# ...    st.header("A dog")
# ...    st.image("https://static.streamlit.io/examples/dog.jpg", use_column_width=True)
col1, col2 = st.beta_columns(2)



touch_point_query_df = df[(df['touchPointId'] == touch_point_id)]
#=====================================================================
#Discount Amount timeline
y = touch_point_query_df['tlog.totals.discountAmount.amount']

x = touch_point_query_df['openDateTimeUtc.dateTime']

time = [ pytz.utc.localize(datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ')) for date in x.values ]

# print(time)
data = pd.DataFrame({
  'date': time,
  'Discount Amount $': y.values
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.header("Discounts provided over Time")
st.line_chart(data)
# selected 
'Current Touch Point ID:', touch_point_id
# #============================================================
# #Spending Amount timeline

y = touch_point_query_df['tlog.totals.grandAmount.amount']
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(np.array([int(date.strftime('%Y%m%d')) for date in time]).reshape(-1,1), y)  # perform linear regression
Y_pred = linear_regressor.predict(np.array([int(date.strftime('%Y%m%d')) for date in time]).reshape(-1,1))

data = pd.DataFrame({
  'date': time,
  'Purchase Amount($)': y.values,
  "Regression curve": Y_pred
})

data = data.rename(columns={'date':'index'}).set_index('index')

st.header("Transaction Amounts over Time")
st.line_chart(data) 
# selected 
'Current Touch Point ID:', touch_point_id

# #====================================================================
#Productwise Sale at a particular Point of Contact
df_prod = pd.io.json.json_normalize(np.hstack(touch_point_query_df['tlog.items']))
# print(df_prod['productName'].values)
# fig, ax = plt.subplots()
# ax.hist(df_prod['productName'].values, bins = len(df_prod['productName'].values))
# print(dir(ax))
# st.pyplot(fig)
# print(df_prod['productName'].value_counts())
st.header("Items Purchases at the given Touchpoint ID")
features = np.array(['feature 1', 'feature 2', 'feature 3'])
features_importances = np.array([.5, .25, .4])
products = df_prod['productName']
# print(np.array(df.value_counts().index))
chart_data = pd.DataFrame()
chart_data['Items'] = np.array(products.value_counts().index)
chart_data['Frequency'] = np.array(df_prod['productName'].value_counts().values)

chart_data
chart_v1 = alt.Chart(chart_data).mark_bar().encode(
x='Items',
y='Frequency')
st.write("", "", chart_v1)



# #Querying the location ID 
# #===================================================================
# location_id = input("Enter the location id: ") 
# print(location_id)

st.title("Infographics for given Location ID")
st.header("Discounts given over time") 
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
time = [ pytz.utc.localize(datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ')) for date in x.values ]
# time[-1].tzinfo = 'EST'
print((time[0].strftime("%z")))
data = pd.DataFrame({
  'date': time,
  'Discount Amount($)': y.values
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.line_chart(data)
# selected 
'Current Location ID:', location_id

# #============================================================
# #Spending Amount timeline
st.header("Transaction Amounts over Time")
y = location_query_df['tlog.totals.grandAmount.amount']

linear_regressor.fit(np.array([int(date.strftime('%Y%m%d')) for date in time]).reshape(-1,1), y)  # perform linear regression
Y_pred = linear_regressor.predict(np.array([int(date.strftime('%Y%m%d')) for date in time]).reshape(-1,1))

data = pd.DataFrame({
  'date': time,
  'Transaction Amount($)': y.values,
  "Regression Curve":Y_pred
})

data = data.rename(columns={'date':'index'}).set_index('index')
st.line_chart(data) 

# selected 
'Current Location ID:', location_id
# #============================================================
# #Productwise Sale at a particular location
df_prod = pd.io.json.json_normalize(np.hstack(location_query_df['tlog.items']))
# print(df_prod['productName'])
# fig, ax = plt.subplots()
# x = df_prod['productName']
# x.value_counts().plot(ax=ax, kind='bar')
# plt.show()
st.header("Items Purchases at a Location ID")
features = np.array(['feature 1', 'feature 2', 'feature 3'])
features_importances = np.array([.5, .25, .4])
products = df_prod['productName']
# print(np.array(df.value_counts().index))
chart_data = pd.DataFrame()
chart_data['Items'] = np.array(products.value_counts().index)
chart_data['Frequency'] = np.array(df_prod['productName'].value_counts().values)
chart_data
chart_v1 = alt.Chart(chart_data).mark_bar().encode(
x='Items',
y='Frequency')
st.write("", "", chart_v1)