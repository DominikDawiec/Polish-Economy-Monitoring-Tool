# setup
import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('Stock forecast dashboard')





# select a time window
import datetime 

def nearest_business_day(DATE: datetime.date):
    """
    Takes a date and transform it to the nearest business day
    """
    if DATE.weekday() == 5:
        DATE = DATE - datetime.timedelta(days=1)

    if DATE.weekday() == 6:
        DATE = DATE + datetime.timedelta(days=1)
    return DATE
      
      
# ------ layout setting---------------------------
window_selection_c = st.sidebar.container() # create an empty container in the sidebar
window_selection_c.markdown("## Insights") # add a title to the sidebar container
sub_columns = window_selection_c.columns(2) #Split the container into two columns for start and end date

# ----------Time window selection-----------------
YESTERDAY=datetime.date.today()-datetime.timedelta(days=1)
YESTERDAY = nearest_business_day(YESTERDAY) #Round to business day

DEFAULT_START=YESTERDAY - datetime.timedelta(days=700)
DEFAULT_START = nearest_business_day(DEFAULT_START)

START = sub_columns[0].date_input("From", value=DEFAULT_START, max_value=YESTERDAY - datetime.timedelta(days=1))
END = sub_columns[1].date_input("To", value=YESTERDAY, max_value=YESTERDAY, min_value=START)

START = nearest_business_day(START)
END = nearest_business_day(END)






# ---------------stock selection------------------
STOCKS = np.array([ "GOOG", "GME", "FB","AAPL",'TSLA'])  
SYMB = window_selection_c.selectbox("select stock", STOCKS)




chart_width = st.expander(label="chart width").slider("", 1000, 2800, 1400) #arguments: label, min, default, max




def show_delta(self):
        """
        Visualize a summary of the stock change over the specified time period
        """
        epsilon = 1e-6 
        i = self.start
        j = self.end
        s = self.data.query("date==@i")['Close'].values[0]
        e = self.data.query("date==@j")['Close'].values[0]

        difference = round(e - s, 2) 
        change = round(difference / (s + epsilon) * 100, 2) #Denominator is always >0
        e = round(e, 2)
        cols = st.columns(2)
        (color, marker) = ("green", "+") if difference >= 0 else ("red", "-")

        cols[0].markdown(
            f"""<p style="font-size: 90%;margin-left:5px">{self.symbol} \t {e}</p>""",
            unsafe_allow_html=True 
        )
        cols[1].markdown(
            f"""<p style="color:{color};font-size:90%;margin-right:5px">{marker} \t {difference} {marker} {change} % </p>""",
            unsafe_allow_html=True
        ) 
        
        
        
        
        
change_c = st.sidebar.container()
with change_c:
    stock.show_delta()
    
    
    
    
    
    
    
import yfinance as yf
import datetime
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


class Stock:
    """
    This class enables data loading, plotting and statistical analysis of a given stock,
     upon initialization load a sample of data to check if stock exists. 
        
    """

    def __init__(self, symbol="GOOG"):
       
        self.end = datetime.datetime.today()
        self.start = self.end - datetime.timedelta(days=4)
        self.symbol = symbol
        self.data = self.load_data(self.start, self.end)

    @st.cache(show_spinner=False) #Using st.cache allows st to load the data once and cache it. 
    def load_data(self, start, end, inplace=False):
        """
        takes a start and end dates, download data do some processing and returns dataframe
        """

        data = yf.download(self.symbol, start, end + datetime.timedelta(days=1))
        #Check if there is data
        try:
            assert len(data) > 0
        except AssertionError:
            print("Cannot fetch data, check spelling or time window")
        data.reset_index(inplace=True)
        data.rename(columns={"Date": "datetime"}, inplace=True)
        data["date"] = data.apply(lambda raw: raw["datetime"].date(), axis=1)

        data = data[["date", 'Close']]
        if inplace:
            self.data = data
            self.start = start
            self.end = end
            return True
        return data

    def plot_raw_data(self, fig):
        """
        Plot time-serie line chart of closing price on a given plotly.graph_objects.Figure object
        """
        fig = fig.add_trace(
            go.Scatter(
                x=self.data.date,
                y=self.data['Close'],
                mode="lines",
                name=self.symbol,
            )
        )
        return fig
    

    @staticmethod
    def nearest_business_day(DATE: datetime.date):
        """
        Takes a date and transform it to the nearest business day, 
        static because we would like to use it without a stock object.
        """
        if DATE.weekday() == 5:
            DATE = DATE - datetime.timedelta(days=1)

        if DATE.weekday() == 6:
            DATE = DATE + datetime.timedelta(days=1)
        return DATE
    
    def show_delta(self):
        """
        Visualize a summary of the stock change over the specified time period
        """
        epsilon = 1e-6
        i = self.start
        j = self.end
        s = self.data.query("date==@i")['Close'].values[0]
        e = self.data.query("date==@j")['Close'].values[0]

        difference = round(e - s, 2)
        change = round(difference / (s + epsilon) * 100, 2)
        e = round(e, 2)
        cols = st.columns(2)
        (color, marker) = ("green", "+") if difference >= 0 else ("red", "-")

        cols[0].markdown(
            f"""<p style="font-size: 90%;margin-left:5px">{self.symbol} \t {e}</p>""",
            unsafe_allow_html=True)
        cols[1].markdown(
            f"""<p style="color:{color};font-size:90%;margin-right:5px">{marker} \t {difference} {marker} {change} % </p>""",
            unsafe_allow_html=True) 
        
        
        
        
import streamlit as st
import datetime
from plotly import graph_objects as go
import numpy as np
import plotly.graph_objects as go
from stock import Stock

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('Stock forecast dashboard')

      
# ------ layout setting---------------------------
window_selection_c = st.sidebar.container() # create an empty container in the sidebar
window_selection_c.markdown("## Insights") # add a title to the sidebar container
sub_columns = window_selection_c.columns(2) #Split the container into two columns for start and end date

# ----------Time window selection-----------------
YESTERDAY=datetime.date.today()-datetime.timedelta(days=1)
YESTERDAY = Stock.nearest_business_day(YESTERDAY) #Round to business day

DEFAULT_START=YESTERDAY - datetime.timedelta(days=700)
DEFAULT_START = Stock.nearest_business_day(DEFAULT_START)

START = sub_columns[0].date_input("From", value=DEFAULT_START, max_value=YESTERDAY - datetime.timedelta(days=1))
END = sub_columns[1].date_input("To", value=YESTERDAY, max_value=YESTERDAY, min_value=START)

START = Stock.nearest_business_day(START)
END = Stock.nearest_business_day(END)
# ---------------stock selection------------------
STOCKS = np.array([ "GOOG", "GME", "FB","AAPL",'TSLA'])  # TODO : include all stocks
SYMB = window_selection_c.selectbox("select stock", STOCKS)

chart_width = st.expander(label="chart width").slider("", 1000, 2800, 1400)


# # # ------------------------Plot stock linechart--------------------

fig=go.Figure()
stock = Stock(symbol=SYMB)
stock.load_data(START, END, inplace=True)
fig = stock.plot_raw_data(fig)

#---------------styling for plotly-------------------------
fig.update_layout(
            width=chart_width,
            margin=dict(l=0, r=0, t=0, b=0, pad=0),
            legend=dict(
                x=0,
                y=0.99,
                traceorder="normal",
                font=dict(size=12),
            ),
            autosize=False,
            template="plotly_dark",
)

st.write(fig)

change_c = st.sidebar.container()
with change_c:
    stock.show_delta()
