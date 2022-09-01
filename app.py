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

# avaiable variables
RGDP = 'NGDPRSAXDCPLQ'
CPI = 'POLCPIALLMINMEI'
CPIEnergy = 'POLCPIENGQINMEI'
Working_Age_Population = 'LFWA64TTPLQ647N'
RegisteredUnemploymentRate = 'LMUNRRTTPLM156S'


def main_plot(fname):
  dfx = fred.observations(fname)
  
  dfx = pd.DataFrame.from_dict(dfx['observations'])
  dfx['date'] = pd.to_datetime(dfx['date'])
  dfx['value'] = pd.to_numeric(dfx['value'],errors = 'coerce')
  
  fig = px.line(dfx, x='date', y='value', title='Time Series with Range Slider and Selectors')
  st.plotly_chart(fig, use_container_width=True)
    
  most_recent = dfx['value'].iat[-1]
  deltax = most_recent-1
  st.metric(label="Most Recent Value", value=most_recent, delta=deltax)
  
  #dfxz = dfx[["date","value"]]
  #st.dataframe(dfxz)
  


#page_names = ['X', 'Y', 'Inflation']
#page = st.selectbox('Navigation', page_names)
#st.write('Wybrany wskaźnik: ', page)

#if page == 'X':
  main_plot(X)
  
df = fred.search('NGDPRSAXDCPLQ')
dfx = pd.DataFrame.from_dict(df['seriess'])
st.dataframe(dfx)

