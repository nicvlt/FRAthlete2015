import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_excel('assets/SHN_2015.xlsx', engine='openpyxl')
    df = df.drop(['SHN_Id'], axis=1)
    df = df.dropna(subset=['Club'])
    df['Sexe'] = df['Sexe'].astype(str)
    df['Sexe'] = df['Sexe'].str.strip()

    return df

def side_bar(text):

    st.sidebar.header("#Dataviz2023efrei")
    st.sidebar.header("*by [Nicolas VIOLOT](https://www.linkedin.com/in/nicolasviolot/)*")