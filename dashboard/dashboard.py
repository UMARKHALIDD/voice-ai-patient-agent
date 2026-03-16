import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/patients"

st.set_page_config(layout="wide")

st.title("Patient Administration Dashboard")

res = requests.get(API_URL)
data = res.json()["data"]

df = pd.DataFrame(data)

search = st.text_input("Search by First Name")

if search:
    df = df[df["first_name"].str.contains(search, case=False)]

st.dataframe(df)