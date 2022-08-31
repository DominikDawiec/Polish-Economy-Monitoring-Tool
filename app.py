import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('Stock forecast dashboard')



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
