import pandas as pd
import numpy as np

import fred
from fredapi import Fred

import streamlit as st
     
import plotly.express as px
import plotly.graph_objects as go

# setting the website details
st.set_page_config(
     page_title="Polish Economic Indicators",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded")

# api key
fred.key('8c3b945500069081b94040df2da12df7')

# downloading list of avaiable variables concerning Poland
available_variables = fred.category_series(32339)
available_variables = pd.DataFrame.from_dict(available_variables['seriess'])
available_variables['subtitle'] = available_variables['title'] + ", FREQUENCY:" + available_variables['frequency'] + ', UNIT:' + available_variables['units'] + ', SEASONAL ADJUSTMENT:' + available_variables['seasonal_adjustment']

# creating list of variables' names for selectbox
list_of_available_variables = available_variables.title.unique()

# creating a function returning variable ID of chosen variable 
def choose_variable(variable):
  chosen_variable = available_variables.loc[available_variables["title"] ==variable]
     
  if chosen_variable.shape[0] > 1:
    sub_chosen_variable = chosen_variable.subtitle.unique()
    chosen_subvariable = st.selectbox('The selected indicator has more variants to choose from:', sub_chosen_variable)
    subvariable = available_variables.loc[available_variables["subtitle"] ==chosen_subvariable]
    choose_variable.ID = subvariable['id'].iat[-1]
  else:
    subvariable = available_variables.loc[available_variables["title"] ==variable]
    choose_variable.ID = subvariable['id'].iat[-1]

# setting the selectbox
chosen_variable_name = st.selectbox('Please select an indicator', list_of_available_variables)
choose_variable(chosen_variable_name)
variable_ID = choose_variable.ID


# Defining functions
# =====================================================================================================

# Function to download data 
def download_data(variable):
    timeseries = fred.observations(variable)
    timeseries = pd.DataFrame.from_dict(timeseries['observations'])
    timeseries['date'] = pd.to_datetime(timeseries['date'])
    timeseries['date'] = timeseries['date'].dt.date
    timeseries['value'] = pd.to_numeric(timeseries['value'],errors = 'coerce')
    timeseries = timeseries.drop(['realtime_start', 'realtime_end'], axis=1)
    download_data.timeseries = timeseries
    
    info_1 = fred.search(variable)
    info_1 = pd.DataFrame.from_dict(info_1['seriess'])
    info_1.replace(r'\s+', np.nan, regex=True)
    download_data.info_1 = info_1
    
    info_2 = fred.series(variable, release=True)
    info_2 = pd.DataFrame.from_dict(info_2['releases'])
    info_1.replace(r'\s+', np.nan, regex=True)
    download_data.info_2 = info_2

# Setting function Creating Plot
def plot():
    with st.container():
         tab1, tab2 = st.tabs(["Historical Chart 📈", "Historical Data 💾"])
         with tab1:
          st.header("Historical Chart 📈")
          fig = px.line(timeseries, x='date', y="value")
          fig.update_layout(
               yaxis_title='Value',
               xaxis_title='Date',
               hovermode="x")
          
          fig.update_xaxes(rangeslider_visible=True)
          
          fig.update_xaxes(
               rangeslider_visible=True,
               rangeselector=dict(
                    buttons=list([
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(count=5, label="5y", step="year", stepmode="backward"),
                         dict(count=10, label="10y", step="year", stepmode="backward"),
                         dict(step="all")])))
          st.plotly_chart(fig, use_container_width=True)
                
    with tab2:
     st.header("Historical Data 💾")
     
     fig = go.Figure(data=[go.Table(header=dict(values=['<b>DATE<b>', '<b>VALUE<b>'], 
                                                line_color='black',
                                                font=dict(color='white'),
                                                align=['left'],
                                                fill_color='#636EFA'),
                                    cells=dict(values=[timeseries['date'], timeseries['value']], 
                                               font=dict(color='black'),
                                               align=['left'],
                                               line_color='black',
                                               fill_color='white'))])
     st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
          st.header("KPIs 📟")
          col1, col2, col3 = st.columns(3)
          col1.metric("Ultimate value", ultimate_value)
          col2.metric("Preultimate value", preultimate_value)
          col3.metric("Percentage change", percentage_change)
        
    with st.container():
          st.header("Details 📇")
        
          values = [['title', 'observation_start', 'observation_end', 'frequency', 'units', 'seasonal_adjustment', 'last_updated', 'link', 'notes'], #1st col
                    [info_1['title'].iat[-1],
                    info_1['observation_start'].iat[-1],
                    info_1['observation_end'].iat[-1],
                    info_1['frequency'].iat[-1],
                    info_1['units'].iat[-1],
                    info_1['seasonal_adjustment'].iat[-1],
                    info_1['last_updated'].iat[-1],
                    info_2['link'].iat[-1],
                    info_1['notes'].iat[-1]]]
          fig = go.Figure(data=[go.Table(
               columnorder = [1,2],
               columnwidth = [100,450],
               header = dict(
                    values = [['<b>CATEGORY</b>'],['<b>DESCRIPTION</b>']],
                    line_color='black',
                    fill_color='#636EFA',
                    align=['left'],
                    font=dict(color='white', size=12),
                    height=40),
               cells=dict(
                    values=values,
                    line_color='black',
                    fill=dict(color=['white', 'white']),
                    align=['left'],
                    font=dict(color='black'),
                    font_size=12,
                    height=30))])
          fig.update_layout(height=550)
          st.plotly_chart(fig, use_container_width=True)

def data_analitics():
     timeseries['natural_log'] = np.log(timeseries['value'])
     timeseries['values'] = timeseries['value']
     timeseries['percentage change'] = timeseries['value'].pct_change().mul(100)
     timeseries['value difference'] = timeseries['value'].diff()
     data_analitics.timeseries = timeseries

def analitical_insights():
     with st.container():
          st.header("Analitical Insights ✨")
          
          unit = st.selectbox('Please select unit', ['values','natural_log','percentage change','value difference'])
          
          fig = px.line(timeseries, x='date', y=unit)
          fig.update_layout(
               yaxis_title='Value',
               xaxis_title='Date',
               hovermode="x")
          
          fig.update_xaxes(rangeslider_visible=True)
          
          fig.update_xaxes(
               rangeslider_visible=True,
               rangeselector=dict(
                    buttons=list([
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(count=5, label="5y", step="year", stepmode="backward"),
                         dict(count=10, label="10y", step="year", stepmode="backward"),
                         dict(step="all")])))
          st.plotly_chart(fig, use_container_width=True)
# =========================================================================================================

download_data(variable_ID)

# saving attributes outside functions
timeseries = download_data.timeseries
info_1 = download_data.info_1
info_2 = download_data.info_2

# creating values for KPIs
ultimate_value = timeseries['value'].iat[-1]
preultimate_value = timeseries['value'].iat[-2]
percentage_change = ((ultimate_value - preultimate_value) / preultimate_value) * 100

plot()

data_analitics()

# saving attribute outside function
timeseries = timeseries = data_analitics.timeseries

analitical_insights()
