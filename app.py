# importing all required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fred
from fredapi import Fred

# key
fred.key('8c3b945500069081b94040df2da12df7')

# page setup
st.set_page_config(page_title="Polish Macroeconomic Indicators", page_icon="📊", initial_sidebar_state="expanded")

# title
st.title('Polish Macroeconomic Indicators')
st.subheader('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')
st.caption('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')



def main_plot(fname):
  # downloading timeseries data from API
  df = fred.observations(fname)
  
  # cleaning the dataset with timeseries
  df = pd.DataFrame.from_dict(df['observations'])
  df['date'] = pd.to_datetime(df['date'])
  df['value'] = pd.to_numeric(df['value'],errors = 'coerce')
  
  # downloading detailed data from API
  dfx = fred.search(fname)
  
  # cleaning detailed data from API
  dfx = pd.DataFrame.from_dict(dfx['seriess'])
 
  # downloading data about source
  dfa = fred.series(fname, release=True)
  
  # cleaning detailed about source
  dfa = pd.DataFrame.from_dict(dfa['releases'])
 
  # creating plot with timeseries
  fig = px.line(df, x='date', y='value', title= dfx['title'].iat[-1])
  st.plotly_chart(fig, use_container_width=True)
  
  # creating KPIs
  st.write('Observation Start:', dfx['observation_start'].iat[-1])
  st.write('Observation End:', dfx['observation_end'].iat[-1])
  st.write('Frequency:', dfx['frequency'].iat[-1])
  st.write('Unit:', dfx['units'].iat[-1])
  st.write('Seasonal Adjustment:', dfx['seasonal_adjustment'].iat[-1])
  st.write('Last Updated:', dfx['last_updated'].iat[-1])
  st.write('Source Link:', dfa['link'].iat[-1])

  # Calculations for KPIs
  last_value = df['value'].iat[-1]
  penultimate_value = df['value'].iat[-2]
  momdiff = ((last_value - penultimate_value)/penultimate_value)*100
  
  # creating KPIs
  st.write('Last Value:', last_value)
  st.write('Penultimate Value:', penultimate_value)
  st.write('MoM Change:', momdiff, "%")

  #st.dataframe(dfx)
  #st.dataframe(df)

dfz = fred.category_series(32339)
dfz = pd.DataFrame.from_dict(dfz['seriess'])
dfz['name'] = dfz['title'] + " (" + dfz['id'] + ")"
dfz.sort_values(by='title')

# categories = dfz.title.unique()
# choose_category = st.selectbox("Choose an economic indicator:", categories)

# main_plot(choose_category)


# dfz.loc[dfz["name"] =="Harmonized Index of Consumer Prices: Overall Index Excluding Energy, Food, Alcohol, and Tobacco for Poland (00XEFDPLM086NEST)", ["id", "name", "notes"]]
categories2 = dfz.title.unique()
choose_category2 = st.selectbox("Choose an economic indicator:", categories2)





def subcategory(y):
  ghb = dfz.loc[dfz["title"] ==y, ["id", "title", "name"]]
  st.dataframe(ghb)

 
categories3 = ('x', 'y')
choose_category3 = st.selectbox("Available variances:", categories3)



def testfunction(x):
  ghb = dfz.loc[dfz["name"] ==x, ["id", "name", "notes"]]
  main_plot(ghb['id'].iat[-1])
  st.write("notes:", ghb['notes'].iat[-1])

 
testfunction(choose_category2)

st.dataframe(dfz)

subcategory(choose_category2)
