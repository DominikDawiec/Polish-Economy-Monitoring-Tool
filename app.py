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
