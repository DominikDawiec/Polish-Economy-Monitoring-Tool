import yfinance as yf
import streamlit as st

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
     



st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Google!
""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GOOGL'





from datetime import datetime

import streamlit as st
from vega_datasets import data

from utils import chart, db

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


st.set_page_config(layout="centered", page_icon="💬", page_title="Commenting app")

# Data visualisation part

st.title("💬 Commenting app")

source = data.stocks()
all_symbols = source.symbol.unique()
symbols = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3])

space(1)

source = source[source.symbol.isin(symbols)]
chart = chart.get_chart(source)
st.altair_chart(chart, use_container_width=True)

space(2)

# Comments part

conn = db.connect()
comments = db.collect(conn)

with st.expander("💬 Open comments"):

    # Show comments

    st.write("**Comments:**")

    for index, entry in enumerate(comments.itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

        is_last = index == len(comments) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ Your comment was successfully posted.")

    space(2)

    # Insert comment

    st.write("**Add your own comment:**")
    form = st.form("comment")
    name = form.text_input("Name")
    comment = form.text_area("Comment")
    submit = form.form_submit_button("Add comment")

    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        db.insert(conn, [[name, comment, date]])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)
