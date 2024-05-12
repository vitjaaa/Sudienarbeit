import glob
import pandas as pd
import os
import re


def Erstelle_Trainingsdaten():

    #Lese die Excel Daten aus dem Ordner Daten/Wetterdaten ein.
    path_Wetter = r'Daten/Wetterdaten'
    Wetterdaten = glob.glob(os.path.join(path_Wetter, "*.xlsx"))

    #Für Jede Datei in Wetterdaten. Nehme Spalte 1-25 und füge sie in eine Liste ein.
    Wetterdaten_24h = []
    Wetterdaten_48h = []
    Wetterdaten_72h = []
    Wetterdaten_96h = []
    for file in Wetterdaten:
        data = pd.read_excel(file)
        Wetterdaten_24h.append(data[1:25])
        Wetterdaten_48h.append(data[26:49])
        Wetterdaten_72h.append(data[50:73])
        Wetterdaten_96h.append(data[74:97])

    #Mache aus dem Array aus Listen nur eine Liste
    Wetterdaten_24h = pd.concat(Wetterdaten_24h)
    Wetterdaten_48h = pd.concat(Wetterdaten_48h)
    Wetterdaten_72h = pd.concat(Wetterdaten_72h)
    Wetterdaten_96h = pd.concat(Wetterdaten_96h)



    def convert_decimal_separator(value):
        """Konvertiert Punkte in Kommata bei Dezimalzahlen."""
        if isinstance(value, str) and '.' in value:
            return value.replace('.', ',')
        return value

    def convert_date_format(date_str):
        """Konvertiert ein Datum im Format DD.MM.YYYY in das Format YYYY-MM-DD."""
        if re.match(r'\d{2}\.\d{2}\.\d{4}', date_str):
            day, month, year = date_str.split('.')
            return f'{year}-{month}-{day}'
        return date_str

    # Ordner mit den CSV-Dateien
    input_folder = 'Daten/Messdaten_Halle'


    # Liste um die eingelesenen Daten zu speichern
    Messdaten_Halle = []

    # Alle CSV-Dateien im Ordner durchgehen
    for csv_file in os.listdir(input_folder):
        if csv_file.endswith('.csv'):
            # Datei-Pfad erstellen
            file_path = os.path.join(input_folder, csv_file)

            # CSV-Datei mit pandas einlesen
            df = pd.read_csv(file_path, sep=";", decimal='.')

            # Dezimaltrennzeichen konvertieren
            df = df.apply(lambda x: x.map(convert_decimal_separator) if x.dtype == 'object' else x)

            # Datum und Zeit kombinieren und konvertieren
            df['date'] = df['date'].apply(convert_date_format)
            df['datetime'] = df['date'] + " " + df['time']
            df = df.drop(columns=['date', 'time'])  # Ursprüngliche Spalten entfernen

            # DataFrame zur Liste hinzufügen
            Messdaten_Halle.append(df)

    # Alle eingelesenen Daten kombinieren
    combined_data = pd.concat(Messdaten_Halle, ignore_index=True)

    # Datetime-Spalte an die erste Position verschieben
    cols = ['datetime'] + [col for col in combined_data if col != 'datetime']
    combined_data = combined_data[cols]




    # Ordner mit den CSV-Dateien
    input_folder = 'Daten/Messdaten_Zaun'


    # Liste um die eingelesenen Daten zu speichern
    Messdaten_Zaun = []

    # Alle CSV-Dateien im Ordner durchgehen
    for csv_file in os.listdir(input_folder):
        if csv_file.endswith('.csv'):
            # Datei-Pfad erstellen
            file_path = os.path.join(input_folder, csv_file)

            # CSV-Datei mit pandas einlesen
            df = pd.read_csv(file_path, sep=";", decimal='.')

            # Dezimaltrennzeichen konvertieren
            df = df.apply(lambda x: x.map(convert_decimal_separator) if x.dtype == 'object' else x)

            # Datum und Zeit kombinieren und konvertieren
            df['date'] = df['date'].apply(convert_date_format)
            df['datetime'] = df['date'] + " " + df['time']
            df = df.drop(columns=['date', 'time'])  # Ursprüngliche Spalten entfernen

            # DataFrame zur Liste hinzufügen
            Messdaten_Zaun.append(df)

    # Alle eingelesenen Daten kombinieren
    combined_data = pd.concat(Messdaten_Zaun, ignore_index=True)

    # Datetime-Spalte an die erste Position verschieben
    cols = ['datetime'] + [col for col in combined_data if col != 'datetime']
    combined_data = combined_data[cols]


    Messdaten_Zaun = pd.concat(Messdaten_Zaun)
    Messdaten_Halle = pd.concat(Messdaten_Halle)

    #ändere die Reihenfolge der Spalten in Messdaten_Halle und Messdaten_Zaun in datetime, speed, direction
    Messdaten_Halle = Messdaten_Halle[['datetime', 'speed', 'direction']]
    Messdaten_Zaun = Messdaten_Zaun[['datetime', 'speed', 'direction']]





    #Wandle in Datetime um
    Messdaten_Halle['datetime'] = pd.to_datetime(Messdaten_Halle['datetime'])
    Messdaten_Zaun['datetime'] = pd.to_datetime(Messdaten_Zaun['datetime'])

    Messdaten_Halle['speed'] = pd.to_numeric(Messdaten_Halle['speed'], errors='coerce')
    Messdaten_Halle['direction'] = pd.to_numeric(Messdaten_Halle['direction'], errors='coerce')

    Messdaten_Zaun['speed'] = pd.to_numeric(Messdaten_Zaun['speed'], errors='coerce')
    Messdaten_Zaun['direction'] = pd.to_numeric(Messdaten_Zaun['direction'], errors='coerce')




    # Bilde die 1h Mittelwerte für speed und direction
    Messdaten_Halle = Messdaten_Halle.resample('1h', on='datetime').mean()
    Messdaten_Zaun = Messdaten_Zaun.resample('1h', on='datetime').mean()

    #Schmeiße Zeilen mit Nan Werten raus
    Messdaten_Halle = Messdaten_Halle.dropna()
    Messdaten_Zaun = Messdaten_Zaun.dropna()

    # Benenne Zeit in datetime um
    Wetterdaten_24h['Zeit'] = pd.to_datetime(Wetterdaten_24h['Zeit'])
    Wetterdaten_48h['Zeit'] = pd.to_datetime(Wetterdaten_48h['Zeit'])
    Wetterdaten_72h['Zeit'] = pd.to_datetime(Wetterdaten_72h['Zeit'])
    Wetterdaten_96h['Zeit'] = pd.to_datetime(Wetterdaten_96h['Zeit'])

    #Benenne die Spalte Zeit in datetime um
    Wetterdaten_24h = Wetterdaten_24h.rename(columns={'Zeit': 'datetime'})
    Wetterdaten_48h = Wetterdaten_48h.rename(columns={'Zeit': 'datetime'})
    Wetterdaten_72h = Wetterdaten_72h.rename(columns={'Zeit': 'datetime'})
    Wetterdaten_96h = Wetterdaten_96h.rename(columns={'Zeit': 'datetime'})

    # Füge Wetterdaten und Messdaten zusammen mit datetime
    Trainingsdaten_Halle_24h = pd.merge(Messdaten_Halle, Wetterdaten_24h, on='datetime')
    Trainingsdaten_Halle_48h = pd.merge(Messdaten_Halle, Wetterdaten_48h, on='datetime')
    Trainingsdaten_Halle_72h = pd.merge(Messdaten_Halle, Wetterdaten_72h, on='datetime')
    Trainingsdaten_Halle_96h = pd.merge(Messdaten_Halle, Wetterdaten_96h, on='datetime')

    Trainingsdaten_Zaun_24h = pd.merge(Messdaten_Zaun, Wetterdaten_24h, on='datetime')
    Trainingsdaten_Zaun_48h = pd.merge(Messdaten_Zaun, Wetterdaten_48h, on='datetime')
    Trainingsdaten_Zaun_72h = pd.merge(Messdaten_Zaun, Wetterdaten_72h, on='datetime')
    Trainingsdaten_Zaun_96h = pd.merge(Messdaten_Zaun, Wetterdaten_96h, on='datetime')


    #Speichere die Daten in einem Ordner
    Trainingsdaten_Halle_24h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Halle_24h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Halle_48h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Halle_48h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Halle_72h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Halle_72h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Halle_96h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Halle_96h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Zaun_24h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Zaun_24h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Zaun_48h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Zaun_48h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Zaun_72h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Zaun_72h.csv', index=False, sep=';', decimal=',')
    Trainingsdaten_Zaun_96h.to_csv('Daten/Trainingsdaten/Trainingsdaten_Zaun_96h.csv', index=False, sep=';', decimal=',')

    


if __name__ == '__main__':
    Erstelle_Trainingsdaten()