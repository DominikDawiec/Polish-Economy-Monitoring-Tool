#import streamlit as st 
import pandas as pd
import plotly.graph_objects as go
#from streamlit_lottie 
import json

df = pd.read_csv('/kaggle/input/netflix-shows/netflix_titles.csv')
df.head(2)
