import Hilfsfunktionen
import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

st.set_page_config(page_title="Windenergieanlage", page_icon="🌬️", layout="wide", initial_sidebar_state="expanded")

WetterDaten_Halle, WetterDaten_Zaun = Hilfsfunktionen.VorhersagenTreffen()
WetterDaten_Halle['Zeit'] = pd.to_datetime(WetterDaten_Halle['Zeit']).dt.tz_convert('Europe/Berlin')
WetterDaten_Zaun['Zeit'] = pd.to_datetime(WetterDaten_Zaun['Zeit']).dt.tz_convert('Europe/Berlin')
# Transformiere die Zeit in ein lesbares Format
WetterDaten_Halle['Zeit'] = WetterDaten_Halle['Zeit'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Chart für die Windgeschwindigkeit
st.markdown("<h1 style='text-align: center;'>Windvorhersage Halle</h1>", unsafe_allow_html=True)
chart_data = WetterDaten_Halle.set_index('Zeit')[['Windgeschwindigkeit (m/s)', 'Windgeschwindigkeitvorhersage (m/s)']]
melted_data = chart_data.reset_index().melt(id_vars='Zeit', var_name='Variable', value_name='Wert')

chart = alt.Chart(melted_data).mark_line().encode(
    x=alt.X('Zeit:T', title='Datum und Uhrzeit'),
    y=alt.Y('Wert:Q', title='Windgeschwindigkeit [m/s]'),
    color=alt.Color('Variable:N', scale=alt.Scale(scheme='category10'))  
).properties(
    width=0,
    height=800,
)
st.altair_chart(chart.interactive(), use_container_width=True)

# Chart für die Windrichtung
st.markdown("<h1 style='text-align: center;'>Windrichtung Halle</h1>", unsafe_allow_html=True)
chart_data = WetterDaten_Halle.set_index('Zeit')[['Windrichtung (°)', 'Windrichtungvorhersage (°)']]
melted_data = chart_data.reset_index().melt(id_vars='Zeit', var_name='Variable', value_name='Wert')

chart = alt.Chart(melted_data).mark_line().encode(
    x=alt.X('Zeit:T', title='Datum und Uhrzeit'),
    y=alt.Y('Wert:Q', title='Windrichtung [°]'),
    color=alt.Color('Variable:N', scale=alt.Scale(scheme='category10'))  
).properties(
    width=0,
    height=800,
)
st.altair_chart(chart.interactive(), use_container_width=True)

# Chart für die Windgeschwindigkeit
st.markdown("<h1 style='text-align: center;'>Windvorhersage Zaun</h1>", unsafe_allow_html=True)
chart_data = WetterDaten_Zaun.set_index('Zeit')[['Windgeschwindigkeit (m/s)', 'Windgeschwindigkeitvorhersage (m/s)']]
melted_data = chart_data.reset_index().melt(id_vars='Zeit', var_name='Variable', value_name='Wert')

chart = alt.Chart(melted_data).mark_line().encode(
    x=alt.X('Zeit:T', title='Datum und Uhrzeit'),
    y=alt.Y('Wert:Q', title='Windgeschwindigkeit [m/s]'),
    color=alt.Color('Variable:N', scale=alt.Scale(scheme='category10'))  
).properties(
    width=0,
    height=800,
)
st.altair_chart(chart.interactive(), use_container_width=True)

# Chart für die Windrichtung
st.markdown("<h1 style='text-align: center;'>Windrichtung Zaun</h1>", unsafe_allow_html=True)
chart_data = WetterDaten_Zaun.set_index('Zeit')[['Windrichtung (°)', 'Windrichtungvorhersage (°)']]
melted_data = chart_data.reset_index().melt(id_vars='Zeit', var_name='Variable', value_name='Wert')

chart = alt.Chart(melted_data).mark_line().encode(
    x=alt.X('Zeit:T', title='Datum und Uhrzeit'),
    y=alt.Y('Wert:Q', title='Windrichtung [°]'),
    color=alt.Color('Variable:N', scale=alt.Scale(scheme='category10'))  
).properties(
    width=0,
    height=800,
)
st.altair_chart(chart.interactive(), use_container_width=True)