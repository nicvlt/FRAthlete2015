import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from utils import load_data, side_bar

# Page config
st.set_page_config(
    page_title="Gender Analysis",
    page_icon="👥",
    layout="wide"
)
side_bar("👥 Gender Analysis")

# Load data
df = load_data()

# Page content
st.write('## Single Variable Analysis')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Datnai", "Sexe", "Catlib", "FedNom", "Discipline"])
with tab1:
    st.write('#### Year of Birth')
    st.bar_chart(df['Datnai'].value_counts())
    
with tab2:
    st.write('#### Gender')
    st.bar_chart(df['Sexe'].value_counts())

with tab3:
    st.write('#### Category')
    st.bar_chart(df['Catlib'].value_counts())
    
with tab4:
    st.write('#### Federation')
    st.bar_chart(df['FedNom'].value_counts().sort_index())
    
with tab5:
    st.write('#### Discipline')
    st.write('There are {} unique disciplines.'.format(len(df['Discipline'].unique())))
    discipline_federation = df.groupby('FedNom')['Discipline'].unique()
    st.dataframe(discipline_federation, use_container_width=True)
    
st.write('## Multiple Variable Analysis')
col1, col2 = st.columns([1, 1])

with col1:
    import plotly.express as px

    st.write('#### Distribution of Year of Birth by Gender')
    gender_year = df.groupby(['Datnai', 'Sexe']).size().reset_index(name='counts')
    fig1 = px.bar(gender_year, x='Datnai', y='counts', color='Sexe', barmode='group', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    st.plotly_chart(fig1)

    st.write('#### Distribution of Category by Gender')
    gender_category = df.groupby(['Catlib', 'Sexe']).size().reset_index(name='counts')
    fig2 = px.bar(gender_category, x='Catlib', y='counts', color='Sexe', barmode='group', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    st.plotly_chart(fig2)
    "For each years and each category, the distribution of women is half the men's"


with col2:
    st.write('#### Gender Gap by Federation')
    gender_gap = df.groupby('FedNom')['Sexe'].value_counts().unstack().fillna(0)
    gender_gap['GenderGap'] = (gender_gap['M'] - gender_gap['F'])/gender_gap.sum(axis=1)
    gender_gap_sorted = gender_gap.sort_values(by='GenderGap', ascending=False)


    fig3 = px.bar(gender_gap_sorted, x=gender_gap_sorted.index, y='GenderGap')
    fig3.update_layout(xaxis_tickangle=-90, xaxis_title='Federation', yaxis_title='Gender Gap (Males - Females)/(Total of Federation)')
    st.plotly_chart(fig3)

    st.write('- If M is significantly greater than F, the result will be close to 1.')
    st.write('- If F is significantly greater than M, the result will be close to -1.')
    st.write('- If M and F are approximately equal, the result will be close to 0.')
    """We can consider that Federations (sports) between 0.6 and 0.4 represent a "non-biaised" sport due to the number of women being around 60% to 40% the number of men in all categories."""
    "Meaning that sports like Billard (Pool), Football Americain (American Football) or Automobile are very men-driven sports. Whereas Gymnastique (Gymnastics), Bowling or Natation (Swimming) are very women-driven sports. (Let's not forget that Billard doesn't have a lot of licenses which highly influences this result)"