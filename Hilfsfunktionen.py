import requests
import pandas as pd
import configparser
import os
import joblib


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
api_key = config['API_EINSTELLUNGEN']['api_key']
latitude = config['API_EINSTELLUNGEN']['latitude']
longitude = config['API_EINSTELLUNGEN']['longitude']


def vorhersageAnfordern():
    try:
        url = f"https://api.tomorrow.io/v4/weather/forecast?location={latitude},{longitude}&units=metric&apikey={api_key}"

        response = requests.get(url)


        if response.status_code == 200:

            data = response.json()

            for item in data['timelines']['hourly']:
                time = item['time']
                values = item['values']
                humidity = values['humidity']
                pressure_surface_level = values['pressureSurfaceLevel']
                rain_intensity = values['rainIntensity']
                temperature = values['temperature']
                wind_direction = values['windDirection']
                wind_gust = values['windGust']
                wind_speed = values['windSpeed']



            df = pd.DataFrame([
                {
                'Zeit': item['time'],
                'Temperatur (°C)': item['values']['temperature'],
                'Luftfeuchtigkeit (%)': item['values']['humidity'],
                'Luftdruck (hPa)': item['values']['pressureSurfaceLevel'],
                'Regenmenge (mm)': item['values']['rainIntensity'],
                'Windgeschwindigkeit (m/s)': item['values']['windSpeed'],
                'Windrichtung (°)': item['values']['windDirection'],
                'Windböen (m/s)': item['values']['windGust'],
                }
                for item in data['timelines']['hourly']
            ])

            # Speicher das DataFrame in einer CSV-Datei
            df.to_csv(os.path.join(os.path.dirname(__file__), 'Wetterdaten.csv'), sep=';', decimal=',', index=False)

            return df
        else:
            print("Fehler beim Abrufen der Wetterdaten.")
            time.sleep(10)

            vorhersageAnfordern()

    except Exception as e:
        print("Fehler beim Abrufen der Wetterdaten:", e)
        time.sleep(10)
        vorhersageAnfordern()




def VorhersagenTreffen():
    # Wetterdaten.csv in ein dataframe einlesen
    WetterDaten = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Wetterdaten.csv'), sep=';', decimal=',')

    #WetterDaten = vorhersageAnfordern()

    X = WetterDaten[['Temperatur (°C)', 'Luftfeuchtigkeit (%)', 'Luftdruck (hPa)', 'Regenmenge (mm)', 'Windgeschwindigkeit (m/s)', 'Windrichtung (°)', 'Windböen (m/s)']]
    Halle_Richtung_24h = joblib.load(os.path.join(os.path.dirname(__file__), 'KI', 'Halle_Richtung_24h.pkl'))
    Zaun_Richtung_24h = joblib.load(os.path.join(os.path.dirname(__file__), 'KI', 'Zaun_Richtung_24h.pkl'))
    Halle_Windgeschwindigkeit_24h = joblib.load(os.path.join(os.path.dirname(__file__), 'KI', 'Halle_Wind_24h.pkl'))
    Zaun_Windgeschwindigkeit_24h = joblib.load(os.path.join(os.path.dirname(__file__), 'KI', 'Zaun_Wind_24h.pkl'))

    vorhersageRichtungHalle = Halle_Richtung_24h.predict(X)
    vorhersageRichtungZaun = Zaun_Richtung_24h.predict(X)
    vorhersageWindHalle = Halle_Windgeschwindigkeit_24h.predict(X)
    vorhersageWindZaun = Zaun_Windgeschwindigkeit_24h.predict(X)

    # Füge Vorhersage Richtung und Wetterdaten zusammen
    WetterDaten_Zaun= WetterDaten
    WetterDaten_Halle= WetterDaten
    WetterDaten_Halle['Windrichtungvorhersage (°)'] = vorhersageRichtungHalle
    WetterDaten_Halle['Windgeschwindigkeitvorhersage (m/s)'] = vorhersageWindHalle
    WetterDaten_Zaun['Windrichtungvorhersage (°)'] = vorhersageRichtungZaun
    WetterDaten_Zaun['Windgeschwindigkeitvorhersage (m/s)'] = vorhersageWindZaun
    


    # Füge RichtungsvorhersagenHalle in die Daten ein
    #WetterDaten['Windrichtungvorhersage (°)'] = RichtungsvorhersagenHalle

    #print(WetterDaten)

 

    return WetterDaten_Halle, WetterDaten_Zaun







if __name__ == "__main__":
    VorhersagenTreffen()
    print("Fertig")

