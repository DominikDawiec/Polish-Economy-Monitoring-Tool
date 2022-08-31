import yfinance as yf
import streamlit as st
import pandas as pd

st.set_page_config(page_title="A/B Testing App", page_icon="📊", initial_sidebar_state="expanded")



st.title('This is a title')
st.header('This is a header')
st.subheader('This is a subheader')
st.caption('This is a string that explains something above.')

st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

st.metric(label="Gas price", value=4, delta=-0.5,
     delta_color="inverse")

df = pd.read_csv('indexData.csv')
st.dataframe(df)




option = st.selectbox(
     'How would you like to be contacted?',
     ('X', 'Y', 'Z'))

If option == 'X':
     st.header('X')
     st.subheader('Description')
     st.write('It is a sigmoid function with a characteristic "S"-shaped curve.')








  

# source = df
# all_symbols = source.Index.unique()
# symbols = st.selectbox("Choose stocks to visualize", all_symbols)




st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Google!
""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GOOGL'
