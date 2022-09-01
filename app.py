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
# st.dataframe(df)   dziala

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

  
  
import plotly.figure_factory as ff
# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
         hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)
