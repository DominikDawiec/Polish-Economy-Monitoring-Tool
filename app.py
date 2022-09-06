import pandas as pd
import numpy as np

import fred
from fredapi import Fred

import streamlit as st
     
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go

from datetime import date

import matplotlib.pyplot as plt
import warnings

from pylab import rcParams  

import cufflinks

from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm

import xlsxwriter

# import warnings
warnings.filterwarnings('ignore')

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
          vrect = st.selectbox('Please select vrect', ['none (default)', 'economic crises','political parties'])

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
          
          if vrect == 'none (default)':
               st.plotly_chart(fig, use_container_width=True)
               
          elif vrect == 'economic crises':
               
               fig.add_vrect(x0="2020-01-01", x1="2020-06-31", 
                             annotation_text="Covid-19 Crisis", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               fig.add_vrect(x0="2007-12-01", x1="2009-09-31", 
                             annotation_text="Global Crisis", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               fig.add_vrect(x0="2001-02-01", x1="2002-02-31", 
                             annotation_text="Internet Bubble Crisis", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               st.plotly_chart(fig, use_container_width=True)
               
          elif vrect == 'political parties':
               
               fig.add_vrect(x0="1995-03-07", x1="1997-10-31", 
                             annotation_text="SLD-PSL", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               fig.add_vrect(x0="1997-11-01", x1="2001-10-19", 
                             annotation_text="AWS-UW", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="green", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2001-10-19", x1="2004-05-02", 
                             annotation_text="SLD-UP-PSL", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="red", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2004-05-02", x1="2005-10-19", 
                             annotation_text="SLD-UP", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="yellow", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2005-10-31", x1="2007-11-16", 
                             annotation_text="PiS-SO-LPR", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="grey", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2007-11-17", x1="2015-11-13", 
                             annotation_text="PO-PSL", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               today = date.today()
               d1 = today.strftime("%Y-%m-%d")
          
               fig.add_vrect(x0="2015-11-14", x1=d1, 
                             annotation_text="PiS", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman"),
                             fillcolor="red", opacity=0.25, line_width=0)
               
               st.plotly_chart(fig, use_container_width=True)
               
               
        
def forecast():
     st.header("Forecasts 🔮")
     init_notebook_mode(connected=True)
     def testStationarity(ts):
          dftest = adfuller(ts)
          dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
          for key,value in dftest[4].items():
               dfoutput['Critical Value (%s)'%key] = value
          return dfoutput
     
     testStationarity(timeseries.value)
     
     mod = sm.tsa.statespace.SARIMAX(timeseries,
                                     order=(1, 1, 0),
                                     seasonal_order=(0, 1, 1, 12),
                                     enforce_stationarity=False,
                                     enforce_invertibility=False)
     results = mod.fit()
     
     pred = results.get_prediction(start=pd.to_datetime('2016-01-01'), dynamic=False)
     pred_ci = pred.conf_int()
     
     pred_ci['predicted'] = (pred_ci['lower value'] + pred_ci['upper value'])/2
     pred_ci['observed'] = timeseries['value']
     pred_ci['diff, %%'] = ((pred_ci['predicted'] / pred_ci['observed'])-1) * 100
     
     forecast.prec_ci_1 = pred_ci
     
     # Get forecast 3 years ahead in future
     pred_uc = results.get_forecast(steps=36)
     
     # Get confidence intervals of forecasts
     pred_ci = pred_uc.conf_int()
     
     pred_ci['Mean'] = (pred_ci['lower value'] + pred_ci['upper value'])/2
     
     forecast.prec_ci = pred_ci
     
     forecast.Test_Stationary = testStationarity(timeseries.value)
     
     forecast.Results_Summary = results.summary()

def forecast_plot():
     
     agree = st.checkbox('Show line')
          
     fig = go.Figure([
          go.Scatter(
               name='predicted value',
               x=pred_ci.index,
               y=pred_ci['Mean'],
               mode='lines',
               line=dict(color='red'),
          ),
          go.Scatter(
               name='upper bound',
               x=pred_ci.index,
               y=pred_ci['upper value'],
               mode='lines',
               marker=dict(color="#444"),
               line=dict(width=0),
               showlegend=False
          ),
          go.Scatter(
               name='lower bound',
               x=pred_ci.index,
               y=pred_ci['lower value'],
               marker=dict(color="#444"),
               line=dict(width=0),
               mode='lines',
               fillcolor='rgba(68, 68, 68, 0.3)',
               fill='tonexty',
               showlegend=False
          ),
          go.Scatter(
               name='historical value',
               x=timeseries.index,
               y=timeseries['value'],
               mode='lines',
               line=dict(color='rgb(31, 119, 180)'),
          )
     ])
     fig.update_layout(
          yaxis_title='Value',
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
     
     with st.expander("See training plot"):
          fig = go.Figure([
               go.Scatter(
                    name='Training Details',
                    x=pred_ci_1.index,
                    y=pred_ci_1['predicted'],
                    mode='markers',
                    line=dict(color='green'),
               ),
               go.Scatter(
                    name='training upper value',
                    x=pred_ci_1.index,
                    y=pred_ci_1['upper value'],
                    mode='lines',
                    marker=dict(color="grey"),
                    line=dict(width=0),
                    showlegend=False
               ),
               go.Scatter(
                    name='training lower value',
                    x=pred_ci_1.index,
                    y=pred_ci_1['lower value'],
                    marker=dict(color="grey"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(68, 68, 68, 0.3)',
                    fill='tonexty',
                    showlegend=False
               ),
               go.Scatter(
                    name='historical value',
                    x=timeseries.index,
                    y=timeseries['value'],
                    mode='lines',
                    line=dict(color='blue'),
               )
          ])
          fig.update_layout(
               yaxis_title='Value',
               hovermode="x")
          
          st.plotly_chart(fig, use_container_width=True)
          
          with st.expander("See model details"):
               st.dataframe(Test_Stationary)
               st.write(Results_Summary)

          

def download():
     with st.container():
          st.header("Download data 📥")
          st.info('Work in progress - not ready YET', icon="ℹ️")
          
          # creating excel file
          buffer = io.BytesIO()
          
          # Create a Pandas Excel writer using XlsxWriter as the engine.
          with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
          # Write each dataframe to a different worksheet.
          pred_ci_1.to_excel(writer, sheet_name='Sheet1')
          Test_Stationary.to_excel(writer, sheet_name='Sheet2')
          # Close the Pandas Excel writer and output the Excel file to the buffer
          writer.save()
          
          st.download_button(
               label="Download Excel Worksheet",
               data=buffer,
               file_name="pandas_multiple.xlsx",
               mime="application/vnd.ms-excel"
          )
          
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
timeseries = data_analitics.timeseries

analitical_insights()

# cleaning timeseries df before forecast
timeseries = timeseries.set_index(['date'])
timeseries = timeseries.drop(columns=['values','natural_log','percentage change','value difference'])

forecast()

pred_ci_1 = forecast.prec_ci_1
pred_ci = forecast.prec_ci 
Test_Stationary = forecast.Test_Stationary # dataframe
Results_Summary = forecast.Results_Summary # st write

forecast_plot()

download()


