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

def side_bar(title):

    # make a markdown text with as title the argument 'title'. Add a section break after the title and add "Author: " as text with a link to my LinkedIn profile https://www.linkedin.com/in/nicolasviolot/ clickable on my name.
    st.sidebar.markdown(f'# {title}')
    st.sidebar.markdown('# Author')
    st.sidebar.markdown('This dashboard was made by [Nicolas VIOLOT](https://www.linkedin.com/in/nicolasviolot/).')
    st.sidebar.markdown('# More information')
    st.sidebar.markdown('[My GitHub profile](https://github.com/nicvlt)')
    st.sidebar.markdown('[Repo of this project](https://github.com/nicvlt/FRAthlete2015)')
    st.sidebar.markdown('#DataViz2023EFREI')