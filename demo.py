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

st.title('My first app')

# table
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

# colorful chart
chart_data = pd.DataFrame(
  np.random.randn(20, 3),
  columns=['a', 'b', 'c'])
st.line_chart(chart_data)

# SF map
map_data = pd.DataFrame(
  np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
  columns=['lat', 'lon'])
st.map(map_data)

# checkbox to optionally show colorful graph
if st.checkbox('Show dataframe'):
  chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
  st.line_chart(chart_data)

# sidebar filter
option = st.sidebar.selectbox(
  'Which number do you like best?',
  df['first column'])

# shown in main col
'You selected:', option

# button that shows text next to it
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
  right_column.write("Woohoo!")

# toggle text for explanations
expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

# counter
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(10):
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

#######################
# new sidebar filters #
#######################

df = pd.DataFrame({
  'first column': ['Politics', 'Public Transportation', 'Population Density', 'Pollution'],
  'second column': [10, 20, 30, 40]
})

# sidebar filter
priority = st.sidebar.selectbox(
  'Which factor is your top priority?',
  df['first column'])

# shown in main col
'You selected:', priority

# show graph based on priority
if priority == 'Pollution':
  map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
  st.map(map_data)
else:
  chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
  st.line_chart(chart_data)