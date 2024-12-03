# -*- coding: utf-8 -*-
"""dashboard.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xiulwUH6Kd6KV8sb3s_OTqOl3HvUqXwy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import json
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from babel.numbers import format_currency
# sns.set(style='dark')

def create_filter_prov_df(df):
    filter_prov = df.sort_values(by="PAGU", ascending=True)
    return filter_prov

def display_map(df):
    # Membuat peta dengan pusat Indonesia
    map = folium.Map(location=[-6.1751, 106.8650], zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')
    
    # Membaca GeoJSON dari file lokal
    geojson_url = 'indonesia-edit.geojson'

    # Membuat Choropleth Map untuk peta Indonesia
    choropleth = folium.Choropleth(
        geo_data=geojson_url,
        data=df,
        columns=['PROVINSI', 'Jumlah Sekolah SD'],  # Menyesuaikan dengan kolom di DataFrame
        key_on='feature.properties.state',  # Menyesuaikan dengan properti GeoJSON 'state'
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Jumlah Sekolah SD'
    )
    choropleth.geojson.add_to(map)

    # Menambahkan informasi tambahan pada setiap provinsi di GeoJSON
    df_indexed = df.set_index('PROVINSI')  # Indeks menggunakan 'PROVINSI' untuk pencocokan
    
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['state'].lower()  # Nama provinsi di GeoJSON
        if state_name in df_indexed.index:
            feature['properties']['population'] = 'Jumlah Sekolah SD: ' + str(df_indexed.loc[state_name, 'Jumlah Sekolah SD'])

    # Menambahkan tooltip pada GeoJSON untuk menampilkan informasi yang relevan
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['state', 'population'], labels=False)  # Menggunakan 'state' dan 'population' sebagai tooltip
    )

    # Menampilkan peta di Streamlit
    st_map = st_folium(map, width=700, height=450)

    # Menangani interaksi dengan peta, seperti klik pada provinsi
    state_name = ''
    if st_map.get('last_active_drawing'):
        state_name = st_map['last_active_drawing']['properties']['state']
    
    return state_name
saya memakai koding ini berhasil tapi warna nya hitam
def display_map(df):
    # Create a map with the center of Indonesia
    map = folium.Map(location=[-6.1751, 106.8650], zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')
    
    # Read GeoJSON from a local file
    geojson_url = 'indonesia-edit.geojson'
    # Create a Choropleth Map for the Indonesian map
    choropleth = folium.Choropleth(
        geo_data=geojson_url,
        data=df,
        columns=['PROVINCE', 'Number of Elementary Schools'], # Adjust to columns in DataFrame
        key_on='feature.properties.state', # Matches GeoJSON property 'state'
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Number of Elementary Schools'
    )
    choropleth.geojson.add_to(map)
    # Added additional information on each province in GeoJSON
    df_indexed = df.set_index('PROVINCE') # Index uses 'PROVINCE' for matching
    
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['state'].lower() # Province name in GeoJSON
        if state_name in df_indexed.index:
            feature['properties']['population'] = 'Number of Elementary Schools: ' + str(df_indexed.loc[state_name, 'Number of Elementary Schools'])
    # Added a tooltip to GeoJSON to display relevant information
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['state', 'population'], labels=False) # Use 'state' and 'population' as tooltips
    )
    # Displays the map in Streamlit
    st_map = st_folium(map, width=700, height=450)
    # Handle interactions with the map, such as clicking on provinces
    state_name = ''
    if st_map.get('last_active_drawing'):
        state_name = st_map['last_active_drawing']['properties']['state']
    
    return state_name


# menyiapkan data all_data
all_df = pd.read_csv('data_set_2023.csv')

filter_prov_df = create_filter_prov_df(all_df)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo_IDE.png")

pd.DataFrame(filter_prov_df)

st.subheader('APBN 2023')

col1, col2 = st.columns(2)

with col1:
    total_provinsi = filter_prov_df['PROVINSI'].count()
    st.metric("Total Provinsi", value=total_provinsi)

with col2:
    total_pagu = filter_prov_df['PAGU'].sum()
    total_pagu_formatted = f"{int(total_pagu / 1e12)} T"
    st.metric("Total PAGU", value=total_pagu_formatted)

plt.figure(figsize=(10, 8))
plt.barh(filter_prov_df['PROVINSI'], filter_prov_df['PAGU'].astype(str).apply(lambda x: x[:-12]),   color=[ "#78B3CE" if pagu == filter_prov_df['PAGU'].max() else "#C9E6F0" for pagu in filter_prov_df['PAGU']])
plt.xlabel('PAGU (Triliun)')
plt.ylabel('Provinsi')
plt.title('Pagu APBN 2023 per Provinsi')
plt.tight_layout()
st.pyplot(plt)

geojson_url = 'indonesia-edit.geojson'

m = folium.Map(location=[-6.1751, 106.8650], zoom_start=5)
all_df['PROVINSI'] = all_df['PROVINSI'].str.lower()

folium.Choropleth(
    geo_data=geojson_url,
    data=all_df,
    columns=['PROVINSI', 'Jumlah Sekolah SD'],
    key_on="feature.properties.state", 
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Jumlah Sekolah SD"
)
 
state_name = display_map(all_df)
st.write(f'Provinsi yang dipilih: {state_name}')
