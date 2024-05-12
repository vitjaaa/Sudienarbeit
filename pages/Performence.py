import streamlit as st
import os
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="Windenergieanlage", page_icon="🌬️", layout="wide", initial_sidebar_state="expanded")

# Lade die Testdaten
Test_Halle_Richtung_24h = pd.read_csv('Daten\Testdaten\TestHalle_Richtung_24h_Testdaten.csv', sep=';', decimal=',')
Test_Zaun_Richtung_24h = pd.read_csv('Daten\Testdaten\TestZaun_Richtung_24h_Testdaten.csv', sep=';', decimal=',')
Test_Halle_Speed_24h = pd.read_csv('Daten\Testdaten\TestHalle_Wind_24h_Testdaten.csv', sep=';', decimal=',')
Test_Zaun_Speed_24h = pd.read_csv('Daten\Testdaten\TestZaun_Wind_24h_Testdaten.csv', sep=';', decimal=',')

#Lade die KI Modelle
Halle_Richtung_24h = joblib.load('KI\Halle_Richtung_24h.pkl')
Zaun_Richtung_24h = joblib.load('KI\Zaun_Richtung_24h.pkl')
Zaun_Speed_24h = joblib.load('KI\Zaun_Wind_24h.pkl')
Halle_Speed_24h = joblib.load('KI\Halle_Wind_24h.pkl')

#Vorhersage der Windrichtung
vorhersage_Richtung_Halle = Halle_Richtung_24h.predict(Test_Halle_Richtung_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']])
vorhersage_Richtung_Zaun = Zaun_Richtung_24h.predict(Test_Zaun_Richtung_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']])
#Vorhersage der Windgeschwindigkeit
vorhersage_Speed_Halle = Halle_Speed_24h.predict(Test_Halle_Speed_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']])
vorhersage_Speed_Zaun = Zaun_Speed_24h.predict(Test_Zaun_Speed_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']])
#Berechne die RSME Werte
RSME_Richtung_Halle = np.sqrt(np.mean((vorhersage_Richtung_Halle - Test_Halle_Richtung_24h['direction'])**2))
RSME_Richtung_Zaun = np.sqrt(np.mean((vorhersage_Richtung_Zaun - Test_Zaun_Richtung_24h['direction'])**2))
RSME_Speed_Halle = np.sqrt(np.mean((vorhersage_Speed_Halle - Test_Halle_Speed_24h['speed'])**2))
RSME_Speed_Zaun = np.sqrt(np.mean((vorhersage_Speed_Zaun - Test_Zaun_Speed_24h['speed'])**2))
#Berechne die Score Werte
Score_Richtung_Halle = Halle_Richtung_24h.score(Test_Halle_Richtung_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']], Test_Halle_Richtung_24h['direction'])
Score_Richtung_Zaun = Zaun_Richtung_24h.score(Test_Zaun_Richtung_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']], Test_Zaun_Richtung_24h['direction'])
Score_Speed_Halle = Halle_Speed_24h.score(Test_Halle_Speed_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']], Test_Halle_Speed_24h['speed'])
Score_Speed_Zaun = Zaun_Speed_24h.score(Test_Zaun_Speed_24h[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']], Test_Zaun_Speed_24h['speed'])

# Erstelle einen Button mit RSME und Score Werten Berechnen
if st.button('Berechne RSME und Score Werte'):
    # Schreibe die Werte in die Tabelle
    st.write('Halle Windgeschwindigkeit')
    st.write('Score: ', Score_Speed_Halle)
    st.write('RSME: ', RSME_Speed_Halle)
    st.write('Halle Windrichtung')
    st.write('Score: ', Score_Richtung_Halle)
    st.write('RSME: ', RSME_Richtung_Halle)

    # Schreibe das neben die Tabelle
    st.write('Zaun Windgeschwindigkeit')
    st.write('Score: ', Score_Speed_Zaun)
    st.write('RSME: ', RSME_Speed_Zaun)
    st.write('Zaun Windrichtung')
    st.write('Score: ', Score_Richtung_Zaun)
    st.write('RSME: ', RSME_Richtung_Zaun)

# Erstelle mit Altair ein Residual Plot
if st.button('Erstelle Residual Plot'):
    import altair as alt
    # Erstelle ein Dataframe mit den Vorhersagen und den Testdaten
    Residual_Halle_Speed = pd.DataFrame({'Vorhersage': vorhersage_Speed_Halle, 'Testdaten': Test_Halle_Speed_24h['speed']})
    Residual_Halle_Richtung = pd.DataFrame({'Vorhersage': vorhersage_Richtung_Halle, 'Testdaten': Test_Halle_Richtung_24h['direction']})
    Residual_Zaun_Speed = pd.DataFrame({'Vorhersage': vorhersage_Speed_Zaun, 'Testdaten': Test_Zaun_Speed_24h['speed']})
    Residual_Zaun_Richtung = pd.DataFrame({'Vorhersage': vorhersage_Richtung_Zaun, 'Testdaten': Test_Zaun_Richtung_24h['direction']})
    # Erstelle die Plots
    chart1 = alt.Chart(Residual_Halle_Speed).mark_circle().encode(
        x='Vorhersage',
        y='Testdaten'
    ).properties(
        title='Residual Plot Halle Windgeschwindigkeit'
    )
    chart2 = alt.Chart(Residual_Halle_Richtung).mark_circle().encode(
        x='Vorhersage',
        y='Testdaten'
    ).properties(
        title='Residual Plot Halle Windrichtung'
    )
    chart3 = alt.Chart(Residual_Zaun_Speed).mark_circle().encode(
        x='Vorhersage',
        y='Testdaten'
    ).properties(
        title='Residual Plot Zaun Windgeschwindigkeit'
    )
    chart4 = alt.Chart(Residual_Zaun_Richtung).mark_circle().encode(
        x='Vorhersage',
        y='Testdaten'
    ).properties(
        title='Residual Plot Zaun Windrichtung'
    )
    # Ornde die Plots in einem 2x2 Grid an
    st.altair_chart(alt.vconcat(chart1, chart2, chart3, chart4), use_container_width=True)
# Erstelle mit Altair ein Histogramm
                                               

                                                     