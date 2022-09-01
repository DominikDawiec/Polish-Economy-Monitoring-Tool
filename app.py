import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="A/B Testing App", page_icon="📊", initial_sidebar_state="expanded")



st.title('This is a title')
st.header('This is a header')
st.subheader('This is a subheader')
st.caption('This is a string that explains something above.')

# st.metric(label="Temperature", value="70 °F", delta="1.2 °F")


df = pd.read_csv('indexData.csv')
# st.dataframe(df)   dziala

NYA = df[df.Index.isin(['NYA'])]
NYA1 = NYA[["Date", "Close"]]
# st.dataframe(NYA1)   dziala
# st.table(NYA1)    dziala ale pokazuje cala dlugosc
df = NYA1
dfx = NYA1

most_recent = df['Close'].iat[-1]
deltax = most_recent-1
st.caption(most_recent)
st.metric(label="Most Recent Value", value=most_recent, delta=deltax)


page_names = ['X', 'Y', 'NYA']
page = st.selectbox('Navigation', page_names)
st.write('Choosen', page)

if page == 'X':
  st.write('test X')
  
if page == 'Y':
  plt.plot(df.Date, df.Close)
  st.pyplot()
  
if page == 'NYA':
  st.line_chart(NYA1.Close)

  
  
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)
