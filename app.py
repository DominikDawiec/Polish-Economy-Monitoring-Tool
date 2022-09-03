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
  timeseries.df = df

  dfw = fred.search(id)
  dfw = pd.DataFrame.from_dict(dfw['seriess'])
  timeseries.dfw = dfw
  
  dfa = fred.series(id, release=True)
  dfa = pd.DataFrame.from_dict(dfa['releases'])
  timeseries.dfa = dfa
     
 
with st.container():
     # creating a selectbox
     fname = st.selectbox('Please select an indicator', dfx)

function1(fname)

id = function1.bye

st.write('after doing both functions I have got')
st.write('variable id', id)

timeseries(id)

df = timeseries.df
dfw = timeseries.dfw
dfa = timeseries.dfa

with st.container():
     tab1, tab2, tab3 = st.tabs(["📈 Chart", "🗃 Data", "Data 2"])

     with tab1:
          st.header("First plot")
          fig = px.line(df, x='date', y='value')
          fig.update_xaxes(rangeslider_visible=True)
          fig.update_xaxes(
               rangeslider_visible=True,
               rangeselector=dict(
                    buttons=list([
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(count=5, label="5y", step="year", stepmode="backward"),
                         dict(count=10, label="10y", step="year", stepmode="backward"),
                         dict(step="all")
                    ])
               )
          )
          
          st.plotly_chart(fig, use_container_width=True)
          
     with tab2:
          st.header("Second plot")
          fig = px.bar(df, x='date', y='value')
          fig.update_xaxes(rangeslider_visible=True)
          fig.update_xaxes(
               rangeslider_visible=True,
               rangeselector=dict(
                    buttons=list([
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(count=5, label="5y", step="year", stepmode="backward"),
                         dict(count=10, label="10y", step="year", stepmode="backward"),
                         dict(step="all")
                    ])
               )
          )
          st.plotly_chart(fig, use_container_width=True)

     with tab3:
          st.header("Data")
          fig = go.Figure(data=[go.Table(header=dict(values=['<b>DATE<b>', '<b>VALUE<b>'], 
                                                     line_color='black',
                                                     font=dict(color='white'),
                                                     align=['left'],
                                                     fill_color='#636EFA'),
                                         cells=dict(values=[df['date'], df['value']], 
                                                    font=dict(color='black'),
                                                    align=['left'],
                                                    line_color='black',
                                                    fill_color='white'))
                               ])
          st.plotly_chart(fig, use_container_width=True)
          
with st.container():
     ultimate_value = df['value'].iat[-1]
     preultimate_value = df['value'].iat[-2]
     percentage_change = ((ultimate_value - preultimate_value) / preultimate_value) * 100
     
     col1, col2, col3 = st.columns(3)
     with col1:
          fig = go.Figure(go.Indicator(
          mode = "number",
          value = ultimate_value,
          title = {"text": "Ultimate Value<br><span style='font-size:0.8em;color:gray'>"},
          domain = {'x': [1, 1], 'y': [1, 1]}))
          st.plotly_chart(fig, use_container_width=True)

     with col2:
          fig = go.Figure(go.Indicator(
          mode = "number",
          value = preultimate_value,
          title = {"text": "Preultimate Value<br><span style='font-size:0.8em;color:gray'>"},
          domain = {'x': [1, 1], 'y': [1, 1]}))
          st.plotly_chart(fig, use_container_width=True)

     with col3:
          fig = go.Figure(go.Indicator(
          mode = "number",
          value = percentage_change,
          title = {"text": "Percentage Change<br><span style='font-size:0.8em;color:gray'>"},
          domain = {'x': [1, 1], 'y': [1, 1]}))
          st.plotly_chart(fig, use_container_width=True)
    
