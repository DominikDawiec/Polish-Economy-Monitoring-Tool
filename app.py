# importing all required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fred
fred.key('8c3b945500069081b94040df2da12df7')

#page setup
st.set_page_config(page_title="A/B Testing App", page_icon="📊", initial_sidebar_state="expanded")

# title
st.title('Polish economy viewer')
st.subheader('Ta strona ma na celu przdstawienie wskaźników ekonomicznych dla Polski w czasie rzeczywistym')
st.caption('Kod z każdym zapytaniem łączy się z API w celu pobrania aktualnego df a następnie zwizualizowania go')

# st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

Real Gross Domestic Product for Poland = 'NGDPRSAXDCPLQ'
Consumer Price Index: All Items for Poland = 'POLCPIALLMINMEI'
3-Month or 90-day Rates and Yields: Interbank Rates for Poland = 'IR3TIB01PLM156N'
Harmonized Index of Consumer Prices: Gas for Poland = 'CP0452PLM086NEST'
Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for Poland = 'IRLTLT01PLM156N'
Gross Domestic Product for Poland = 'MKTGDPPLA646NWDB'
Real Residential Property Prices for Poland = 'QPLR628BIS'
Consumer Price Index: Energy for Poland = 'POLCPIENGQINMEI'
Current Price Gross Domestic Product in Poland = 'POLGDPNADSMEI'
Working Age Population: Aged 15-64: All Persons for Poland = 'LFWA64TTPLQ647N'
Registered Unemployment Rate for Poland = 'LMUNRRTTPLM156S'
M3 for Poland = 'MABMM301PLA189S'
Domestic Producer Prices Index: Manufacturing for Poland = 'POLPPDMMINMEI'
Constant GDP per capita for Poland = 'NYGDPPCAPKDPOL'
Household Debt to GDP for Poland = 'HDTGPDPLQ163N'
National Currency to US Dollar Exchange Rate: Average of Daily Rates for Poland = 'CCUSMA02PLM618N'
  
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
  


page_names = ['X', 'Y', 'Inflation']
page = st.selectbox('Navigation', page_names)
st.write('Wybrany wskaźnik: ', page)

if page == 'X':
  main_plot(X)
  
if page == 'Y':
 main_plot(Y)
  
if page == 'Inflation':
  main_plot(Inflation)
