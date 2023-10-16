import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
from utils import load_data, side_bar

# Page config
st.set_page_config(
    page_title="Age Analysis",
    page_icon="👴",
    layout="wide"
)
side_bar("👴 Age Analysis")

# Load data
df = load_data()

# Page content
col1, col2 = st.columns([1, 1])
df['Age'] = 2015 - df['Datnai']
age_range = df.groupby('Catlib')['Age'].agg(['min', 'max'])
age_range['AgeRange'] = age_range['min'].astype(str) + '-' + age_range['max'].astype(str)
age_range['AgeMean'] = (age_range['min'] + age_range['max'])/2
age_range['Mode'] = df.groupby('Catlib')['Age'].agg(lambda x: x.value_counts().index[0])
age_range = age_range.drop(['min', 'max'], axis=1)
age_range = age_range.reset_index()
st.write('#### Category with Age Range')
st.dataframe(age_range, use_container_width=True)

with col1:
    hist_senior_age = df['Age'].loc[df['Catlib'] == 'Senior']
    hist_elite_age = df['Age'].loc[df['Catlib'] == 'Elite']
    hist_espoir_age = df['Age'].loc[df['Catlib'] == 'Espoir']
    hist_jeune_age = df['Age'].loc[df['Catlib'] == 'Jeune']
    hist_data = [hist_senior_age, hist_elite_age, hist_espoir_age, hist_jeune_age]

    group_labels = ['Senior', 'Elite', 'Espoir', 'Jeune']
    st.write('#### Age Distribution by Category')
    fig = ff.create_distplot(hist_data, group_labels, bin_size=1)
    fig.update_xaxes(title_text='Age')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write('#### Count of Athletes by Category')
    pie_data = df.groupby('Catlib')['Age'].count()
    pie_data = pie_data.reset_index()
    pie_data.columns = ['Category', 'Count']
    fig = px.pie(pie_data, values='Count', names='Category', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)