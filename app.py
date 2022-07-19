import streamlit as st
from datetime import date

import yfinance as yf
from plotly import graph_objs as go

# Here you can use markdown language to make your app prettier
st.write("""
# Financial App
""")

# We will use Amazon stocks
stock = 'AMZN'

# Get stock data
get_stock_data = yf.Ticker(stock)

st.write(get_stock_data)
