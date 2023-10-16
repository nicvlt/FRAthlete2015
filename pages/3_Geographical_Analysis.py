import json
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import folium as fo
from streamlit_folium import folium_static
from utils import load_data

# Page config
st.set_page_config(
    page_title="Geographical Analysis",
    page_icon="🌍",
    layout="wide"
)
st.sidebar.header("🌍 Geographical Analysis")

# Load data
df = load_data()

# Geojson data import and cleaning
geojson_path = 'assets/departements.geojson'
with open(geojson_path, 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)
    
for feature in geojson_data['features']:
    feature['properties']['nom'] = feature['properties']['nom'].upper()
    feature['properties']['nom'] = feature['properties']['nom'].replace('É', 'E')
    feature['properties']['nom'] = feature['properties']['nom'].replace('È', 'E')
    feature['properties']['nom'] = feature['properties']['nom'].replace('Ê', 'E')
    feature['properties']['nom'] = feature['properties']['nom'].replace('À', 'A')
    feature['properties']['nom'] = feature['properties']['nom'].replace('Â', 'A')
    feature['properties']['nom'] = feature['properties']['nom'].replace('Ô', 'O')
    feature['properties']['nom'] = feature['properties']['nom'].replace('Î', 'I')

# Page content
option = st.selectbox(
    'Which map do you want to see',
    ('Elevation Representation of Athletes', 'Density by Department', 'Density by Department (with Federations and Disciplines)'))

if option == 'Elevation Representation of Athletes':
    regions = df['RegionLib'].unique()
    regions = pd.DataFrame(regions, columns=['RegionLib'])
    region_cities = {
        'RHONE-ALPES': 'Lyon',
        'MIDI-PYRENEES': 'Toulouse',
        'PAYS DE LA LOIRE': 'Nantes',
        'LANGUEDOC-ROUSSILLON': 'Montpellier',
        'FRANCHE-COMTE': 'Besançon',
        'ILE-DE-FRANCE': 'Paris',
        'HAUTE-NORMANDIE': 'Rouen',
        'AUVERGNE': 'Clermont-Ferrand',
        'ALSACE': 'Strasbourg',
        'P.A.C.A.': 'Marseille',
        'LORRAINE': 'Nancy',
        'POITOU-CHARENTES': 'Poitiers',
        'BRETAGNE': 'Rennes',
        'BOURGOGNE': 'Dijon',
        'NORD-PAS-DE-CALAIS': 'Lille',
        'AQUITAINE': 'Bordeaux',
        'PICARDIE': 'Amiens',
        'REUNION': 'Saint-Denis',
        'NOUVELLE CALEDONIE': 'Nouméa',
        'CENTRE': 'Orléans',
        'LIMOUSIN': 'Limoges',
        'BASSE-NORMANDIE': 'Caen',
        'CORSE': 'Ajaccio',
        'GUYANE': 'Cayenne',
        'GUADELOUPE': 'Basse-Terre',
        'MARTINIQUE': 'Fort-de-France',
        'MONACO': 'Monaco',
        'ETRANGER': None,
        'CHAMPAGNE-ARDENNE': 'Reims',
        'POLYNESIE FRANCAISE': 'Papeete',
        'WALLIS ET FUTUNA': 'Mata-Utu',
        'ST-PIERRE-ET-MIQUELON': 'Saint-Pierre',
    }
    regions['Préfecture'] = regions['RegionLib'].map(region_cities).fillna(np.nan)
    city_data = {
        'City': [
            'Lyon', 'Toulouse', 'Nantes', 'Montpellier', 'Besançon', 'Paris', 'Rouen', 'Clermont-Ferrand',
            'Strasbourg', 'Marseille', 'Nancy', 'Poitiers', 'Rennes', 'Dijon', 'Lille', 'Bordeaux', 'Amiens',
            'Saint-Denis', 'Nouméa', 'Orléans', 'Limoges', 'Caen', 'Ajaccio', 'Cayenne', 'Basse-Terre',
            'Fort-de-France', 'Monaco', 'Unknown', 'Reims', 'Papeete', 'Mata-Utu', 'Saint-Pierre'
        ],
        'Latitude': [
            45.757814, 43.604652, 47.218371, 43.611015, 47.238952, 48.856697, 49.440459, 45.777221,
            48.584614, 43.296174, 48.692054, 46.580259, 48.117266, 47.321581, 50.629250, 44.837789,
            49.895077, -20.879760, -22.271491, 47.902964, 45.833619, 49.182863, 41.927064, 4.922394,
            15.997088, 14.616065, 43.738418, None, 49.257788, -17.537864, -13.289469, 46.776225
        ],
        'Longitude': [
            4.832011, 1.444209, -1.553621, 3.876831, 6.024780, 2.351462, 1.093965, 3.080258,
            7.750712, 5.369952, 6.187403, 0.340196, -1.677792, 5.041470, 3.057256, -0.579180,
            2.302708, 55.450629, 166.448684, 1.909251, 1.261105, -0.370679, 8.738113, -52.313456,
            -61.725875, -61.058588, 7.424616, None, 4.031926, -149.571708, -176.225505, -56.176071
        ]
    }

    city_df = pd.DataFrame(city_data)
    regions = regions.merge(city_df, left_on='Préfecture', right_on='City', how='left')
    regions.drop('City', axis=1, inplace=True)
    type_format = {
        'REUNION': 'Réunion',
        'NOUVELLE CALEDONIE': 'Nouvelle Calédonie',
        'POLYNESIE FRANCAISE': 'Polynésie Française',
        'WALLIS ET FUTUNA': 'Wallis et Futuna',
        'ST-PIERRE-ET-MIQUELON': 'St-Pierre-et-Miquelon',
        'MARTINIQUE': 'Martinique',
        'GUYANE': 'Guyane',
        'GUADELOUPE': 'Guadeloupe',
        'ETRANGER': None,
    }
    regions['Type'] = regions['RegionLib'].map(type_format).fillna('Metropolitan')
    regions['NumAthletes'] = regions['RegionLib'].map(df['RegionLib'].value_counts())

    regions = regions.dropna()

    center_position = st.radio(
        "Center map on",
        ["Metropolitan", "Réunion", "Nouvelle Calédonie", "Polynésie Française", "Wallis et Futuna", "St-Pierre-et-Miquelon", "Martinique", "Guyane", "Guadeloupe"],
        horizontal=True,
    )

    st.write('There are {} athletes in {}.'.format(regions[regions['Type'] == center_position]['NumAthletes'].sum(), center_position))
    
    center = [46.2276, 2.2137]

    if center_position == "Metropolitan":
        center = [46.2276, 2.2137]
    elif center_position == "Réunion":
        center = [-21.1151, 55.5364]
    elif center_position == "Nouvelle Calédonie":
        center = [-20.9043, 165.6180]
    elif center_position == "Polynésie Française":
        center = [-17.6797, -149.4068]
    elif center_position == "Wallis et Futuna":
        center = [-13.7687, -177.1561]
    elif center_position == "St-Pierre-et-Miquelon":
        center = [46.8852, -56.3159]
    elif center_position == "Martinique":
        center = [14.6415, -61.0242]
    elif center_position == "Guyane":
        center= [3.9339, -53.1258]
    elif center_position == "Guadeloupe":
        center = [16.2650, -61.5510]

    max_range = regions['NumAthletes'].max()
    hexagon_layer = pdk.Layer(
        "HexagonLayer",
        data=regions,
        get_position="[Longitude, Latitude]",
        get_elevation_weight = "NumAthletes",
        radius=70000,
        elevation_scale=100,
        elevation_range=[0, 2203],
        extruded=True,
        pickable=True,
        color = [255, 255, 255],
    )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=center[0],
            longitude=center[1],
            zoom=5,
            pitch=50,
        ),
        layers=[hexagon_layer],
    )
    st.pydeck_chart(deck)
    
    if st.checkbox('Show regions dataframe'):
        st.dataframe(regions, use_container_width=True)

    
elif option == 'Density by Department':
    
    departements = df['DepLib'].unique()
    departements = pd.DataFrame(departements, columns=['DepLib'])
    departements['NumAthletes'] = departements['DepLib'].map(df['DepLib'].value_counts())

    


    m = fo.Map(location=[46.2276, 2.2137], fill_color = 'YlGnBu', zoom_start=6)
    
    fo.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=departements,
        columns=['DepLib', 'NumAthletes'],
        key_on='feature.properties.nom',
        fill_color = 'BuPu',
        fill_opacity=0.7,
        line_opacity=0.2,
        line_weight=2,
        legend_name='Number of Athletes',
        highlight=True,
        tooltip=fo.features.GeoJsonTooltip(fields=['nom'], aliases=['Department'])
    ).add_to(m)

    fo.LayerControl().add_to(m)
    folium_static(m, width=1000, height=800)
    
    if st.checkbox('Show departments dataframe'):
        st.dataframe(departements, use_container_width=True)
    
elif option == 'Density by Department (with Federations and Disciplines)':
    col1, col2 = st.columns([1, 1])     
    with col1:
        all_federations = df['FedNom'].unique()
        federation_choice = st.selectbox(
            'Choose a federation',
            all_federations,
            index=0
        )
        
        all_disciplines_by_federation = df[df['FedNom'] == federation_choice]['Discipline'].unique()
        if len(all_disciplines_by_federation) == 1:
            discipline_choice = all_disciplines_by_federation[0]
            """There is only one discipline for this federation"""
        else:
            discipline_choice = st.radio(
                "Choose a discipline",
                ('All', *all_disciplines_by_federation),
                index=0
            )     
        
    with col2:
        if discipline_choice == 'All':
            departements_federation = df[df['FedNom'] == federation_choice]['DepLib'].value_counts().reset_index()
            departements_federation.columns = ['DepLib', 'NumAthletes']
        else:
            departements_federation = df[(df['FedNom'] == federation_choice) & (df['Discipline'] == discipline_choice)]['DepLib'].value_counts().reset_index()
            departements_federation.columns = ['DepLib', 'NumAthletes']
        
        
        m = fo.Map(location=[46.2276, 2.2137], fill_color = 'YlGnBu', zoom_start=6)
        
        fo.Choropleth(
            geo_data=geojson_data,
            name='choropleth',
            data=departements_federation,
            columns=['DepLib', 'NumAthletes'],
            key_on='feature.properties.nom',
            fill_color = 'BuPu',
            fill_opacity=0.7,
            line_opacity=0.2,
            line_weight=2,
            legend_name='Number of Athletes',
            highlight=True,
            tooltip=fo.features.GeoJsonTooltip(fields=['nom'], aliases=['Department'])
        ).add_to(m)
        
        fo.LayerControl().add_to(m)
        folium_static(m)