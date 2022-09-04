# importing all required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fred
from fredapi import Fred
import xlsxwriter
import io

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
dfz['subtitle'] = dfz['title'] + ", FREQUENCY:" + dfz['frequency'] + ', UNIT:' + dfz['units'] + ', SEASONAL ADJUSTMENT:' + dfz['seasonal_adjustment']

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
  else:
    hjkl = dfz.loc[dfz["title"] ==x]
    function1.bye = hjkl['id'].iat[-1]

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
     
  st.info('You mey choose between three kinds of showing timeseries', icon="ℹ️")


     
 
with st.container():
     st.title('Polish Macroeconomic Indicators')
     
     with st.expander("How to use this web application"):
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

     # creating a selectbox
     fname = st.selectbox('Please select an indicator', dfx)

function1(fname)

id = function1.bye

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
          #x axis
          fig.update_xaxes(visible=False)

          #y axis    
          fig.update_yaxes(visible=False)

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
     st.header("KPIs")
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
    
with st.container():
     st.header("Detailed informations")
     values = [['title', 'observation_start', 'observation_end', 'frequency', 'units', 'seasonal_adjustment', 'last_updated', 'link', 'notes'], #1st col
               [dfw['title'].iat[-1],
               dfw['observation_start'].iat[-1],
               dfw['observation_end'].iat[-1],
                dfw['frequency'].iat[-1],
                dfw['units'].iat[-1],
                dfw['seasonal_adjustment'].iat[-1],
                dfw['last_updated'].iat[-1],
                dfa['link'].iat[-1],
                dfw['notes'].iat[-1]]]
     fig = go.Figure(data=[go.Table(
          columnorder = [1,2],
          columnwidth = [100,450],
          header = dict(
               values = [['<b>CATEGORY</b>'],['<b>DESCRIPTION</b>']],
               line_color='black',
               fill_color='#636EFA',
               align=['left'],
               font=dict(color='white', size=12),
               height=40
          ),
          cells=dict(
          values=values,
          line_color='black',
          fill=dict(color=['white', 'white']),
          align=['left'],
          font=dict(color='black'),
          font_size=12,
          height=30)
     )
                          ])
     fig.update_layout(height=550)
     st.info('You may see more details about choosen variable below', icon="ℹ️")
     st.plotly_chart(fig, use_container_width=True)
  
with st.container():
     st.header("Download data")
     st.info('You download data regarding choosed variable', icon="ℹ️")

     # creating excel file
     buffer = io.BytesIO()
     
     # Create a Pandas Excel writer using XlsxWriter as the engine.
     with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
          # Write each dataframe to a different worksheet.
          df.to_excel(writer, sheet_name='Sheet1')
          dfw.to_excel(writer, sheet_name='Sheet2')
          dfa.to_excel(writer, sheet_name='Sheet3')
          # Close the Pandas Excel writer and output the Excel file to the buffer
          writer.save()
          
          st.download_button(
               label="Download Excel worksheets",
               data=buffer,
               file_name="pandas_multiple.xlsx",
               mime="application/vnd.ms-excel"
          )

          



with st.container():
     st.header("FORECAST")
     st.dataframe(df)

     
   
