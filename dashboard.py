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
import plotly.express as px
import json
from babel.numbers import format_currency
sns.set(style='dark')

def create_filter_prov_df(df):
    filter_prov = df.sort_values(by="PAGU", ascending=True)
    return filter_prov

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    # Membaca file GeoJSON lokal
    with open('indonesia-en.geojson') as f:
        geojson_data = json.load(f)
    
    # Membuat choropleth map menggunakan Plotly Express
    choropleth = px.choropleth(input_df, 
                                geojson=geojson_data,  # Menggunakan data GeoJSON lokal
                                locations=input_id, 
                                color=input_column, 
                                color_continuous_scale=input_color_theme,
                                range_color=(0, input_df[input_column].max()),
                                scope="asia",
                                labels={input_column: input_column}
                               )

    # Memperbarui layout untuk peta
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    
    return choropleth

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
plt.xlim(left=0)
plt.tight_layout()

st.pyplot(plt)

fig = make_choropleth(all_df, 'PROVINSI', 'Jumlah Sekolah SD', 'Viridis')
st.plotly_chart(fig)
