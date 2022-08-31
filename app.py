import yfinance as yf
import streamlit as st
import pandas as pd

st.title('This is a title')
st.header('This is a header')
st.subheader('This is a subheader')
st.caption('This is a string that explains something above.')

st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

st.metric(label="Gas price", value=4, delta=-0.5,
     delta_color="inverse")

option = st.selectbox(
     'How would you like to be contacted?',
     ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)

if 'Email' in option: # If user selects Email  do 👇
    email_id = st.text_input('Enter the email address we should contact: ')
    if email_id: # If user enters email, do 👇
        st.write(f'Please check {email_id} for an email from us!')
     
df = pd.read_csv('indexData.csv')
st.dataframe(df)

source = df
all_symbols = source.Index.unique()
symbols = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3])


source = source[source.symbol.isin(symbols)]
chart = chart.get_chart(source)



st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Google!
""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GOOGL'
