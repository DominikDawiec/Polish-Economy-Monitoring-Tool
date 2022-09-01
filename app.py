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

Inflation = "CP0452PLM086NEST"
X = "A261RL1Q225SBEA"
Y = "CIVPART"

def main_plot(fname):
  st.title("test function")
  dfx = fred.observations(fname)
  
  dfx = pd.DataFrame.from_dict(dfx['observations'])
  dfx['date'] = pd.to_datetime(dfx['date'])
  dfx['value'] = pd.to_numeric(dfx['value'],errors = 'coerce')
  
  fig = px.line(dfx, x='date', y='value', title='Time Series with Range Slider and Selectors')
  st.plotly_chart(fig, use_container_width=True)
    
  most_recent = dfx['value'].iat[-1]
  deltax = most_recent-1
  st.metric(label="Most Recent Value", value=most_recent, delta=deltax)
  
  dfxz = dfx["date","value"]
  st.dataframe(dfxz)
  
  st.title("end function")



page_names = ['X', 'Y', 'Inflation']
page = st.selectbox('Navigation', page_names)
st.write('Wybrany wskaźnik: ', page)

if page == 'X':
  main_plot(X)
  
if page == 'Y':
 main_plot(Y)
  
if page == 'Inflation':
  main_plot(Inflation)
