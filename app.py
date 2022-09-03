# importing all required libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import fred
from fredapi import Fred

# setting the website
st.set_page_config(
     page_title="Polish Economic Indicators",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",
 )

# key
fred.key('8c3b945500069081b94040df2da12df7')

# downloading list of avaiable variables concerning Poland
all_variables = fred.category_series(32339)
all_variables = pd.DataFrame.from_dict(all_variables['seriess'])
all_variables['subtitle'] = all_variables['title'] + ", FREQUENCY.:" + all_variables['frequency'] + ', UNIT:' + all_variables['units'] + ', SEASONAL ADJUSTMENT:' + all_variables['seasonal_adjustment']

# creating a list of variables to select 
all_variables_to_select = all_variables.title.unique()

# defining a function downloading data about choosen variable
def getdata(choosenvariable):
     choosen_variable_name = all_variables.loc[all_variables["title"] == choosenvariable]
     
     # if there is more varians of choosen variable I would like to let user be able to choose one one of them 
     if choosen_variable_name.shape[0] > 1:
          choosen_variable_id = choosen_variable_name.unique()
          choosen_subvariable = st.selectbox('The selected indicator has more variants to choose from:', choosen_variable_id)
          final_variable_id = dfz.loc[dfz["subtitle"] == choosen_subvariable]
        else:
          final_variable_id = dfz.loc[dfz["title"] ==choosenvariable]

          
# creating a selectbox
fname = st.selectbox('Please select an indicator', all_variables_to_select)

choosenvariable(fname)
