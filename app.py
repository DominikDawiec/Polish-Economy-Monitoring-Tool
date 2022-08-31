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




option = st.selectbox(
     'How would you like to be contacted?',
     ('X', 'Y', 'Z'))

If option == 'X':
     st.header('X')
     








  

# source = df
# all_symbols = source.Index.unique()
# symbols = st.selectbox("Choose stocks to visualize", all_symbols)

