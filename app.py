import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="A/B Testing App", page_icon="📊", initial_sidebar_state="expanded")



st.title('This is a title')
st.header('This is a header')
st.subheader('This is a subheader')
st.caption('This is a string that explains something above.')

# st.metric(label="Temperature", value="70 °F", delta="1.2 °F")


df = pd.read_csv('indexData.csv')
# st.dataframe(df)   dziala
df["Date"] = df["Date"].astype("datetime64")


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


import matplotlib.pyplot as plt
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)




import fred
fred.key('8c3b945500069081b94040df2da12df7')
df = fred.observations('CP0452PLM086NEST')
Inflacja = pd.DataFrame.from_dict(df['observations'])
Inflacja['date'] = pd.to_datetime(Inflacja['date'])
Inflacja['value'] = pd.to_numeric(Inflacja['value'],errors = 'coerce')
Inflacja.to_csv('plik2.csv')


df1 = Inflacja
fig = px.line(df1, x='date', y='value', title='Time Series with Range Slider and Selectors')
st.plotly_chart(fig, use_container_width=True)







import plotly.graph_objects as go

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>EXPENSES</b>','<b>Q1</b>','<b>Q2</b>','<b>Q3</b>','<b>Q4</b>'],
    line_color='darkslategray',
    fill_color=headerColor,
    align=['left','center'],
    font=dict(color='white', size=12)
  ),
  cells=dict(
    values=[
      ['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
      [1200000, 20000, 80000, 2000, 12120000],
      [1300000, 20000, 70000, 2000, 130902000],
      [1300000, 20000, 120000, 2000, 131222000],
      [1400000, 20000, 90000, 2000, 14102000]],
    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 11)
    ))
])

st.plotly_chart(fig, use_container_width=True)
