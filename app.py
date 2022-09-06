import pandas as pd
import numpy as np

import fred
from fredapi import Fred

import streamlit as st
     
import plotly.express as px
import plotly.graph_objects as go

# setting the website details
st.set_page_config(
     page_title="Polish Economic Indicators",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded")

# api key
fred.key('8c3b945500069081b94040df2da12df7')

# downloading list of avaiable variables concerning Poland
available_variables = fred.category_series(32339)
available_variables = pd.DataFrame.from_dict(available_variables['seriess'])
available_variables['subtitle'] = available_variables['title'] + ", FREQUENCY:" + available_variables['frequency'] + ', UNIT:' + available_variables['units'] + ', SEASONAL ADJUSTMENT:' + available_variables['seasonal_adjustment']

# creating list of variables' names for selectbox
list_of_available_variables = available_variables.title.unique()

# creating a function returning variable ID of chosen variable 
def choose_variable(variable):
  chosen_variable = available_variables.loc[available_variables["title"] ==variable]
     
  if chosen_variable.shape[0] > 1:
    sub_chosen_variable = chosen_variable.subtitle.unique()
    chosen_subvariable = st.selectbox('The selected indicator has more variants to choose from:', sub_chosen_variable)
    subvariable = available_variables.loc[available_variables["subtitle"] ==chosen_subvariable]
    choose_variable.ID = subvariable['id'].iat[-1]
  else:
    subvariable = available_variables.loc[available_variables["title"] ==variable]
    choose_variable.ID = subvariable['id'].iat[-1]

# setting the selectbox
chosen_variable_name = st.selectbox('Please select an indicator', list_of_available_variables)
choose_variable(chosen_variable_name)
variable_ID = choose_variable.ID
