import requests
import time
import datetime
import pandas as pd
import schedule


api_key = "klfpDs21kW2aOdS9km3dVCZyF4BmzWpW"
latitude = "48.07"
longitude = "11.62"



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

            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H") + ".csv"



            csv_path = f"/home/vitja/Studienarbeit/Wetterdaten/{filename}"
            df.to_csv(csv_path, index=False)

            print("Wetterdaten wurden Abgerufen")
        else:
            print("Fehler beim Abrufen der Wetterdaten.")
            time.sleep(10)
            vorhersageAnfordern()
    except Exception as e:
        print(f'Fehler beim Abrufen der Wetterdaten')

vorhersageAnfordern()



def schedule_job():
    schedule.every().day.at("23:30").do(vorhersageAnfordern)


schedule_job()

# Endlosschleife zum Ausführen des Schedulers
while True:
    schedule.run_pending()
