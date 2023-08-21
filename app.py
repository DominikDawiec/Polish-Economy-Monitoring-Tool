SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

import pandas as pd
import numpy as np

import fred
from fredapi import Fred

import streamlit as st
     
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly.io as pio
pio.templates.default = "plotly"

from datetime import date

import matplotlib.pyplot as plt
import warnings

from pylab import rcParams  

from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm

import xlsxwriter
import io

# import warnings
warnings.filterwarnings('ignore')


# setting the website details
st.set_page_config(
     page_title="Polish Economy Monitoring Tool",
     page_icon="📊",
     initial_sidebar_state="expanded")

# Main page
st.title("📊 Polish Economy Monitoring Tool")
st.subheader("Real-time Monitoring and Analysis of Economic Indicators")
st.write("Welcome to the Polish Economic Dashboard, a tool for tracking and analyzing key economic indicators for Poland. With our app, you can stay up-to-date on the latest trends in the Polish economy and make informed decisions based on real-time data.")

st.subheader("Get Started")
st.write("To start exploring the app, simply select an indicator from the dropdown menu below.")

# api key
fred.key('8c3b945500069081b94040df2da12df7')

# downloading list of avaiable variables concerning Poland
available_variables = fred.category_series(32339)
available_variables = pd.DataFrame.from_dict(available_variables['seriess'])
available_variables['subtitle'] = available_variables['title'] + ", FREQUENCY:" + available_variables['frequency'] + ', UNIT:' + available_variables['units'] + ', SEASONAL ADJUSTMENT:' + available_variables['seasonal_adjustment']
available_variables = available_variables[~available_variables.title.str.contains("(DISCONTINUED)")] # DELETING DISCOUNTED VARIABLES, in the further development I may use option "show DISCOUNTED variables"
available_variables = available_variables[available_variables.last_updated >= '2021-01-01'] # EXCLUDING VARIABLES THAT HAVEN'T BEEN UPDATED SINCE 2020

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
    timeseries.dropna(axis=0,how='any',thresh=None,subset=None,inplace=True)
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
     
     with st.expander("Variable Details"):
          st.subheader("📇 Variable Details")
          
          values = [['title', 'observation_start', 'observation_end', 'frequency', 'units', 'seasonal_adjustment', 'last_updated', 'notes'], #1st col
                    [info_1['title'].iat[-1],
                    info_1['observation_start'].iat[-1],
                    info_1['observation_end'].iat[-1],
                    info_1['frequency'].iat[-1],
                    info_1['units'].iat[-1],
                    info_1['seasonal_adjustment'].iat[-1],
                    info_1['last_updated'].iat[-1],
                    #info_2['link'].iat[-1],
                    info_1['notes'].iat[-1]]]
          fig = go.Figure(data=[go.Table(
               columnorder = [1,2],
               columnwidth = [100,450],
               header = dict(
                    values = [['<b>CATEGORY</b>'],['<b>DESCRIPTION</b>']],
                    line_color='black',
                    fill_color='#808080',
                    align=['left'],
                    font=dict(color='white', size=12),
                    height=40),
               cells=dict(
                    values=values,
                    line_color='black',
                    fill=dict(color=['#F5F5F5', 'white']),
                    align=['left'],
                    font=dict(color='black'),
                    font_size=12,
                    height=30))])
          fig.update_layout(margin=dict(r=5, l=5, t=5, b=0))
          config = {'displayModeBar': False}
          fig.update_yaxes(visible=False, showticklabels=False)
          fig.update_xaxes(visible=False, showticklabels=False)

          st.plotly_chart(fig, config=config, use_container_width=True, height='100%')
     
     with st.container():
          tab1, tab2 = st.tabs(["📈 Historical Chart", "💾 Historical Data"])
          with tab1:
               st.subheader("📈 Historical Chart")
               fig = px.line(timeseries, x='date', y="value")

               fig.update_layout(
               # yaxis_title='Value',
               # xaxis_title='Date',
                    hovermode="x")
          
               fig.update_layout(margin=dict(r=5, l=5, t=5, b=5))
               fig.update_yaxes(visible=False, showticklabels=False)
               config = {'displayModeBar': False}

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
               st.plotly_chart(fig, config=config, use_container_width=True)
                
     with tab2:
     
          st.subheader("💾 Historical Data")

          fig = go.Figure(data=[go.Table(
              header=dict(
                  values=['<b>DATE<b>', '<b>VALUE<b>'],
                  line_color='black',
                  font=dict(color='white'),
                  align=['left'],
                  fill_color='#808080'
              ),
              cells=dict(
                  values=[timeseries['date'], timeseries['value']],
                  font=dict(color='black'),
                  align=['left'],
                  line_color='black',
                  fill_color='white'
              )
          )])

          fig.update_layout(margin=dict(r=5, l=5, t=5, b=5))
          config = {'displayModeBar': False}

          st.plotly_chart(fig, config=config, use_container_width=True)

          
     with st.container():
          st.subheader("📟 Key Performance Indicators")

         # Creating values for KPIs
          ultimate_value = round(timeseries['value'].iat[-1], 2)
          preultimate_value = round(timeseries['value'].iat[-2], 2)
          percentage_change = round(((ultimate_value - preultimate_value) / preultimate_value) * 100, 2)
          min_value = round(timeseries['value'].min(), 2)
          max_value = round(timeseries['value'].max(), 2)

         # Displaying KPIs
          cols = st.columns(5)
          cols[0].metric("Ultimate value", f"{ultimate_value:,}")
          cols[1].metric("Preultimate value", f"{preultimate_value:,}")
          cols[2].metric("Percentage change", f"{percentage_change}%")
          cols[3].metric("Minimum value", f"{min_value:,}")
          cols[4].metric("Maximum value", f"{max_value:,}")


def data_analitics():
     timeseries['values'] = timeseries['value']
     timeseries['percentage change'] = timeseries['value'].pct_change().mul(100)
     timeseries['value difference'] = timeseries['value'].diff()
     data_analitics.timeseries = timeseries

def analitical_insights():
     with st.container():
          st.subheader("✨ Analitical Insights")
          
          unit = st.selectbox('Please select unit', ['values','percentage change','value difference'])
          vrect = st.selectbox('Please select vrect', ['none (default)', 'economic crises','political parties'])

          fig = px.line(timeseries, x='date', y=unit)
          fig.update_traces(line_color='#606bf3')
          fig.update_layout(
               yaxis_title='Value',
               xaxis_title='Date',
               hovermode="x")
          
          fig.update_layout(margin=dict(r=5, l=5, t=5, b=5))
          fig.update_yaxes(visible=False, showticklabels=False)
          config = {'displayModeBar': False}
          
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
               st.plotly_chart(fig, config=config, use_container_width=True)

               
          elif vrect == 'economic crises':
              fig.add_vrect(x0="2020-01-01", x1="2020-06-31", 
                            annotation_text="Covid-19 Crisis", annotation_position="top left",
                            annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                            fillcolor="blue", opacity=0.25, line_width=0)

              fig.add_vrect(x0="2007-12-01", x1="2009-09-31", 
                            annotation_text="Global Crisis", annotation_position="top left",
                            annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                            fillcolor="green", opacity=0.25, line_width=0)

              fig.add_vrect(x0="2001-02-01", x1="2002-02-31", 
                            annotation_text="Internet Bubble Crisis", annotation_position="top left",
                            annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                            fillcolor="red", opacity=0.25, line_width=0)

              st.plotly_chart(fig, config=config, use_container_width=True)

               
          elif vrect == 'political parties':
               
               fig.add_vrect(x0="1995-03-07", x1="1997-10-31", 
                             annotation_text="SLD-PSL", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               fig.add_vrect(x0="1997-11-01", x1="2001-10-19", 
                             annotation_text="AWS-UW", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="green", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2001-10-19", x1="2004-05-02", 
                             annotation_text="SLD-UP-PSL", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="red", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2004-05-02", x1="2005-10-19", 
                             annotation_text="SLD-UP", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="yellow", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2005-10-31", x1="2007-11-16", 
                             annotation_text="PiS-SO-LPR", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="grey", opacity=0.25, line_width=0)
          
               fig.add_vrect(x0="2007-11-17", x1="2015-11-13", 
                             annotation_text="PO-PSL", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="blue", opacity=0.25, line_width=0)
               
               today = date.today()
               d1 = today.strftime("%Y-%m-%d")
          
               fig.add_vrect(x0="2015-11-14", x1=d1, 
                             annotation_text="PiS", annotation_position="top left",
                             annotation=dict(font_size=10, font_family="Times New Roman", textangle=90),
                             fillcolor="red", opacity=0.25, line_width=0)
               
               st.plotly_chart(fig, config=config, use_container_width=True)
               
        
def forecast():
     st.subheader("🔮 Variable Forecast")
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
     with st.container():
          tab1, tab2, tab3 = st.tabs(["📈 Forecast Chart", "💾 Forecast Data", "🤖 Model Details"])
          
          with tab1:
               st.subheader("📈 Forecast Chart")
               st.info('This forecast is based on a seasonal ARIMA model.', icon="ℹ️")
               fig = go.Figure([
                    go.Scatter(
                         name='forecast',
                         x=pred_ci.index,
                         y=pred_ci['Mean'],
                         mode='lines',
                         line=dict(color='#787fde'),),
                    go.Scatter(
                         name='upper bound',
                         x=pred_ci.index,
                         y=pred_ci['upper value'],
                         mode='lines',
                         marker=dict(color="#a4a9ed"),
                         line=dict(width=0),
                         showlegend=False),
                    go.Scatter(
                         name='lower bound',
                         x=pred_ci.index,
                         y=pred_ci['lower value'],
                         marker=dict(color="#a4a9ed"),
                         line=dict(width=0),
                         mode='lines',
                         fillcolor='rgba(68, 68, 68, 0.3)',
                         fill='tonexty',
                         showlegend=False),
                    go.Scatter(
                         name='hist. value',
                         x=timeseries.index,
                         y=timeseries['value'],
                         mode='lines',
                         line=dict(color='#606bf3'),)])
               
               fig.update_layout(hovermode="x")
               
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
               
               fig.update_layout(margin=dict(r=5, l=5, t=5, b=5))
               fig.update_yaxes(visible=False, showticklabels=False)
               config = {'displayModeBar': False}
               
               fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
               
               st.plotly_chart(fig, config=config, use_container_width=True)
               
          with tab2:
               st.subheader("💾 Forecast Data")
               st.info('This forecast is based on a seasonal ARIMA model.', icon="ℹ️")
               
               fig = go.Figure(data=[go.Table(header=dict(values=['<b>DATE<b>', '<b>LOWER VALUE<b>', '<b>UPPER VALUE<b>', '<b>MEAN<b>'], 
                                                          line_color='black',
                                                          font=dict(color='white'),
                                                          align=['left'],
                                                          fill_color='#808080'),
                                              cells=dict(values=[pred_ci.index, pred_ci['lower value'], pred_ci['upper value'], pred_ci['Mean']], 
                                                         font=dict(color='black'),
                                                         align=['left'],
                                                         line_color='black',
                                                         fill_color='white'))])
               fig.update_layout(margin=dict(r=5, l=5, t=5, b=5))
               config = {'displayModeBar': False}
               
               st.plotly_chart(fig, config=config, use_container_width=True)
               
          with tab3:
               # Display the stationary test results
               #st.write('Results of stationary test:')
               #st.write(test_stationary)

               # Display the summary results of the model
               st.write('Summary of the model results:')
               st.code(Results_Summary)

               # Display the forecast confidence interval 1
               st.write('Forecast Confidence Interval 1:')
               st.dataframe(pred_ci_1)

               # Display the forecast confidence interval 2
               st.write('Forecast Confidence Interval 2:')
               st.dataframe(pred_ci)
               
               
def downloading_data():
    with st.container():
        st.subheader("📥 Download Data")
        st.info('You may download data regarding chosen variable', icon="ℹ️")
        
        # create Excel file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # write each dataframe to a different worksheet
            timeseries.to_excel(writer, sheet_name='Time Series Data')
            forecast.prec_ci.to_excel(writer, sheet_name='Precision Intervals')
            forecast.Test_Stationary.to_excel(writer, sheet_name='Stationarity Test Results')
            #forecast.Results_Summary.to_excel(writer, sheet_name='Forecast Summary')
            
            # add additional information to a separate worksheet
            info_df = pd.DataFrame({'Variable Name': [chosen_variable_name],
                                    'Info 1': [info_1],
                                    'Info 2': [info_2]})
            info_df.to_excel(writer, sheet_name='Additional Info')
            
        # close the Pandas Excel writer and output the Excel file to the buffer
        writer.save()
        
        # download button
        st.download_button(
            label="Download Excel worksheets",
            data=buffer,
            file_name=f"{chosen_variable_name}.xlsx",
            mime="application/vnd.ms-excel")


          
# =====================================================================================================



download_data(variable_ID)

# saving attributes outside functions for the further use
timeseries = download_data.timeseries
info_1 = download_data.info_1
info_2 = download_data.info_2

plot()

data_analitics()

# saving attribute outside function for the future use
timeseries = data_analitics.timeseries

analitical_insights()

# cleaning timeseries df before forecast & for the futher use in functions
timeseries_extra = timeseries #for download excel
timeseries = timeseries.set_index(['date'])
timeseries = timeseries.drop(columns=['values','percentage change','value difference'])

forecast()

#saving attributes outside function for further use
pred_ci_1 = forecast.prec_ci_1
pred_ci = forecast.prec_ci 
Test_Stationary = forecast.Test_Stationary # dataframe
Results_Summary = forecast.Results_Summary # st write

forecast_plot()
  
downloading_data() 
