# -*- coding: utf-8 -*-
"""dashboard.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xiulwUH6Kd6KV8sb3s_OTqOl3HvUqXwy
"""

!pip install streamlit babel

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_filter_prov_df(df):
    filter_prov = df[df['PROVINSI'] == df['KAB_KOTA']]
    filter_prov = filter_prov.sort_values(by="PAGU", ascending=True)
    return filter_prov

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
    st.metric("Total PAGU", value=f"Rp {total_pagu:,.0f}")

plt.figure(figsize=(10, 6))
plt.barh(filter_prov_df['PROVINSI'], filter_prov_df['PAGU'].astype(str).apply(lambda x: x[:-12]),   color=[ "#78B3CE" if pagu == filter_prov_df['PAGU'].max() else "#C9E6F0" for pagu in filter_prov_df['PAGU']])
plt.xlabel('PAGU (Triliun)')
plt.ylabel('Provinsi')
plt.title('Pagu APBN 2023 per Provinsi')
plt.xlim(left=0)
plt.tight_layout()
plt.show()