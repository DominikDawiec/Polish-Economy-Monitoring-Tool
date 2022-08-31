import yfinance as yf
import streamlit as st
import pandas as pd

st.set_page_config(page_title="A/B Testing App", page_icon="📊", initial_sidebar_state="expanded")



st.title('This is a title')
st.header('This is a header')
st.subheader('This is a subheader')
st.caption('This is a string that explains something above.')

# st.metric(label="Temperature", value="70 °F", delta="1.2 °F")


df = pd.read_csv('indexData.csv')
st.dataframe(df)

NYA = df[df.Index.isin(['NYA'])]
NYA1 = NYA[["Date", "Close"]]
st.dataframe(NYA1)



page_names = ['X', 'Y', 'NYA']
page = st.selectbox('Navigation', page_names)
st.write('Choosen', page)

if page == 'X':
  st.write('test X')
  
if page == 'Y':
  st.write('test mest Y')
  
if page == 'NYA':
  st.line_chart(NYA1)
