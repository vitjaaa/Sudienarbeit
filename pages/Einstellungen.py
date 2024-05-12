import streamlit as st
import os
import ErstelleKI


# Erstelle einen Button um die KI zu erstellen
if st.button('Erstelle KI'):
    # Erstelle die KI
    Halle_speed_score, Halle_speed_RSME=ErstelleKI.ErstelleForesterspeed('Daten\Trainingsdaten\Trainingsdaten_Halle_24h.csv', 'Halle_Speed_24h')
    Halle_Richtung_score, Halle_Richtung_RSME=ErstelleKI.ErstelleForesterdirection('Daten\Trainingsdaten\Trainingsdaten_Halle_24h.csv', 'Halle_Richtung_24h')
    Zaun_speed_score, Zaun_speed_RSME=ErstelleKI.ErstelleForesterspeed('Daten\Trainingsdaten\Trainingsdaten_Zaun_24h.csv', 'Zaun_Speed_24h')
    Zaun_Richtung_score, Zaun_Richtung_RSME=ErstelleKI.ErstelleForesterdirection('Daten\Trainingsdaten\Trainingsdaten_Zaun_24h.csv', 'Zaun_Richtung_24h')
    st.write('Die KI wurde erfolgreich erstellt.')
    # Erstelle eine Tabelle mit den RSME und Score Werten
    st.write('Halle Windgeschwindigkeit')
    st.write('Score: ', Halle_speed_score)
    st.write('RSME: ', Halle_speed_RSME)
    st.write('Halle Windrichtung')
    st.write('Score: ', Halle_Richtung_score)
    st.write('RSME: ', Halle_Richtung_RSME)

    st.write('Zaun Windgeschwindigkeit')
    st.write('Score: ', Zaun_speed_score)
    st.write('RSME: ', Zaun_speed_RSME)
    st.write('Zaun Windrichtung')
    st.write('Score: ', Zaun_Richtung_score)
    st.write('RSME: ', Zaun_Richtung_RSME)
    

# Erstelle einen Button um den Ordner mit  Daten zu öffnen
if st.button('Öffne Datenordner'):
    os.startfile('Daten')



    

