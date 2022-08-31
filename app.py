import streamlit as st
import pandas as pd
import numpy as np

# Save your FRED API key.
fred.key('8c3b945500069081b94040df2da12df7')



st.title('Polish Macroeconomy App')
dataset = ('Inflacja', 'Stopa bezrobocia', 'Produkt PKB Brutto')
option = st.selectbox('Wybierz interesujący Cię wskaźnik',dataset)


df = fred.observations('CP0452PLM086NEST')
Inflacja = pd.DataFrame.from_dict(df['observations'])
Inflacja['date'] = pd.to_datetime(Inflacja['date'])
Inflacja['value'] = pd.to_numeric(df1['value'],errors = 'coerce')



import plotly.express as px
import pandas as pd

df1 = df1

fig = px.line(df1, x='date', y='value', title='Time Series with Range Slider and Selectors')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.show()
