# importing all required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fred
from fredapi import Fred

# setting the website
st.set_page_config(
     page_title="Polish Economic Indicators",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",
 )

# key
fred.key('8c3b945500069081b94040df2da12df7')

# downloading list of avaiable variables concerning Poland
dfz = fred.category_series(32339)
dfz = pd.DataFrame.from_dict(dfz['seriess'])
dfz['subtitle'] = dfz['title'] + ", FREQ.:" + dfz['frequency'] + ', UNIT:' + dfz['units'] + ', SEAS. ADJ.:' + dfz['seasonal_adjustment']

# creating list of variables' names for selectbox
dfx = dfz.title.unique()

# creating a function returning variable ID of choosen variable 
def function1(x):
  dfh = dfz.loc[dfz["title"] ==x]
  
  if dfh.shape[0] > 1:
    dfxg = dfh.subtitle.unique()
    dfhx = st.selectbox('The selected indicator has more variants to choose from:', dfxg)
    hjkl = dfz.loc[dfz["subtitle"] ==dfhx]
    function1.bye = hjkl['id'].iat[-1]
    st.write(function1.bye) # checker to delete
  else:
    hjkl = dfz.loc[dfz["title"] ==x]
    function1.bye = hjkl['id'].iat[-1]
    st.write(function1.bye) # checker to delete

# creting a function downloading timeseries
def timeseries(x):
  df = fred.observations(x)
  df = pd.DataFrame.from_dict(df['observations'])
  df['date'] = pd.to_datetime(df['date'])
  df['date'] = df['date'].dt.date
  df['value'] = pd.to_numeric(df['value'],errors = 'coerce')
  df = df.drop(['realtime_start', 'realtime_end'], axis=1)
  plotting.df = df

  dfw = fred.search(id)
  dfw = pd.DataFrame.from_dict(dfw['seriess'])
  plotting.dfw = dfw
  
  dfa = fred.series(id, release=True)
  dfa = pd.DataFrame.from_dict(dfa['releases'])
  plotting.dfa = dfa
 
          
# creating a selectbox
fname = st.selectbox('Please select an indicator', dfx)

function1(fname)
id = function1.bye
