# importing all required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import fred
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
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
  df = fred.observations(fname)
  
  #dfx = pd.DataFrame.from_dict(df['observations'])
  dfx=df
  dfx['date'] = pd.to_datetime(dfx['date'])
  dfx['value'] = pd.to_numeric(dfx['value'],errors = 'coerce')
  
  fig = px.line(dfx, x='date', y='value', title='Time Series with Range Slider and Selectors')
  st.plotly_chart(fig, use_container_width=True)
    
  most_recent = dfx['value'].iat[-1]
  deltax = most_recent-1
  st.metric(label="Most Recent Value", value=most_recent, delta=deltax)
  
  st.dataframe(dfx)
  
  st.title("end function")



  
  
  
  
  

page_names = ['X', 'Y', 'Inflation']
page = st.selectbox('Navigation', page_names)
st.write('Wybrany wskaźnik: ', page)

def fred(fname):
  df = fred.observations(fname)
  st.dataframe(df)

fred(page)


#if page == 'X':
  #st.write('test X')
  
#if page == 'Y':
 # plt.plot(df.Date, df.Close)
 # st.pyplot()
  
#if page == 'Inflation':
  #main_plot(Inflation)
  
#main_plot(page)


  
  
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)


arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)







df1 = Inflacja
fig = px.line(df1, x='date', y='value', title='Time Series with Range Slider and Selectors')
st.plotly_chart(fig, use_container_width=True)











df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
               fill_color='lavender',
               align='left'))
])

st.plotly_chart(fig, use_container_width=True)
