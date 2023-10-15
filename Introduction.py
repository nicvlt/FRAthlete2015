import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Introduction",
    page_icon="🧠",
)
st.sidebar.header("🧠 Introduction")

df = pd.read_excel('assets/SHN_2015.xlsx', engine='openpyxl')
df = df.drop(['SHN_Id'], axis=1)
df = df.dropna(subset=['Club'])
df['Sexe'] = df['Sexe'].astype(str)
df['Sexe'] = df['Sexe'].str.strip()

st.sidebar.header("")
st.title('Dashboard: Officially Registered French Athletes in 2015')
st.write('### We are going to analyse a dataset of officially registered French athletes in 2015. The dataset is available on the website of the French Publicly Accessible Data.')
st.write('https://www.data.gouv.fr/fr/datasets/athletes-inscrits-sur-la-liste-des-sportifs-de-haut-niveau-en-2015/')
st.markdown("<br>", unsafe_allow_html=True)

st.write('Here is the first 5 rows of the dataset:', df.head())

st.write('The dataset contains', df.shape[0], 'rows and', df.shape[1], 'columns.')
st.write('Here is a little explanation of the each column:')
data = {
    'Variable': ['SHN_Id', 'Datnai', 'Sexe', 'Catlib', 'FedNom', 'Discipline', 'Club', 'DepLib', 'RegionLib', 'Fin de droits', 'Date début'],
    'Format': ['Texte', 'Numérique', 'Texte; deux modalités possibles: "M" (masculin) ou "F" (féminin)', 'Texte; 6 modalités possibles: "Senior" - "Elite" - "Espoir" - "Jeune" - "Partenaire d\'entrainement" - "Reconversion"', 'Texte', 'Texte', 'Texte', 'Texte', 'Texte', 'Numérique', 'Numérique'],
    'Définition': ['Numéro unique de l’individu', 'Année de naissance de l’individu', 'Sexe de l’individu', 'Catégorie dans laquelle figure l’individu', 'Nom de la fédération à laquelle l’individu est rattaché', 'Nom de la discipline pour laquelle l’individu est reconnu de haut niveau', 'Nom du club dans lequel l’individu est licencié', 'Nom du département auquel le club de l’individu est rattaché', 'Nom de la région à laquelle le club de l’individu est rattaché', 'Date de fin de prise d\'effet de l\'inscription de l’individu sur la liste', 'Date de début de prise d\'effet de l\'inscription de l’individu sur la liste']
}
df_explain = pd.DataFrame(data)
st.table(df_explain)