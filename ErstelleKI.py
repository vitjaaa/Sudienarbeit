import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
import numpy as np
import joblib


def ErstelleForesterspeed(Trainingsdaten, Modellname):
    #Lade die Trainingsdaten
    Trainingsdaten = pd.read_csv(Trainingsdaten, sep=';', decimal=',')
    Trainingsdaten = Trainingsdaten.dropna()
    #Erstelle die Trainingsdaten für die Vorhersage der Windgeschwindigkeit
    X= Trainingsdaten[['Temperatur (°C)','Luftfeuchtigkeit (%)','Luftdruck (hPa)','Regenmenge (mm)', 'Windgeschwindigkeit (m/s)','Windrichtung (°)','Windböen (m/s)']]
    y= Trainingsdaten['speed']
    #Teile die Daten in Trainings- und Testdaten auf
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #Erstelle ein Modell
    model = ExtraTreesRegressor(
    n_estimators=300,
    max_depth=30,
    min_samples_leaf=1,
    min_samples_split=2,
    max_features=3,
    random_state=42)

    #Trainiere das Modell
    model.fit(X_train, y_train)
    #Teste das Modell
    score = model.score(X_test, y_test)
    RSME = np.sqrt(np.mean((model.predict(X_test) - y_test)**2))
    print('Score: ', score)
    print('RSME: ', RSME)
    #Speichere das Modell
    joblib.dump(model, 'KI/'+Modellname+'.pkl')

    test_data = pd.concat([X_test, y_test], axis=1)
    #Speicher die Testdaten mit dem Namen Modellname + '_Testdaten.csv'
    test_data.to_csv('Daten\Testdaten\Test'+Modellname+'_Testdaten.csv', sep=';', decimal=',', index=False)

    return score, RSME


def ErstelleForesterdirection(Trainingsdaten, Modellname):
    #Lade die Trainingsdaten
    Trainingsdaten = pd.read_csv(Trainingsdaten, sep=';', decimal=',')
    Trainingsdaten = Trainingsdaten.dropna()
    #Erstelle die Trainingsdaten für die Vorhersage der Windgeschwindigkeit
    X= Trainingsdaten[['Temperatur (°C)','Luftfeuchtigkeit (%)','Luftdruck (hPa)','Regenmenge (mm)', 'Windgeschwindigkeit (m/s)','Windrichtung (°)','Windböen (m/s)']]
    y= Trainingsdaten['direction']
    #Teile die Daten in Trainings- und Testdaten auf
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #Erstelle ein Modell
    model = ExtraTreesRegressor(
    n_estimators=300,
    max_depth=30,
    min_samples_leaf=1,
    min_samples_split=2,
    max_features=3,
    random_state=42)

    #Trainiere das Modell
    model.fit(X_train, y_train)
    #Teste das Modell
    score = model.score(X_test, y_test)
    RSME = np.sqrt(np.mean((model.predict(X_test) - y_test)**2))
    print('Score: ', score)
    print('RSME: ', RSME)
    #Speichere das Modell
    joblib.dump(model, 'KI/'+Modellname+'.pkl')
    
    test_data = pd.concat([X_test, y_test], axis=1)
    #Speicher die Testdaten mit dem Namen Modellname + '_Testdaten.csv'
    test_data.to_csv('Daten\Testdaten\Test'+Modellname+'_Testdaten.csv', sep=';', decimal=',', index=False)
    
    
    
    return score, RSME


if __name__ == "__main__":
    Halle_Richtung_24h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Halle_24h.csv', 'Halle_Richtung_24h')
    Halle_Richtung_48h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Halle_48h.csv', 'Halle_Richtung_48h')
    Halle_Richtung_72h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Halle_72h.csv', 'Halle_Richtung_72h')
    Halle_Richtung_96h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Halle_96h.csv', 'Halle_Richtung_96h')
    Zaun_Richtung_24h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Zaun_24h.csv', 'Zaun_Richtung_24h')
    Zaun_Richtung_48h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Zaun_48h.csv', 'Zaun_Richtung_48h')
    Zaun_Richtung_72h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Zaun_72h.csv', 'Zaun_Richtung_72h')
    Zaun_Richtung_96h = ErstelleForesterdirection('Daten/Trainingsdaten/Trainingsdaten_Zaun_96h.csv', 'Zaun_Richtung_96h')
    Halle_Wind_24h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Halle_24h.csv', 'Halle_Wind_24h')
    Halle_Wind_48h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Halle_48h.csv', 'Halle_Wind_48h')
    Halle_Wind_72h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Halle_72h.csv', 'Halle_Wind_72h')
    Halle_Wind_96h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Halle_96h.csv', 'Halle_Wind_96h')
    Zaun_Wind_24h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Zaun_24h.csv', 'Zaun_Wind_24h')
    Zaun_Wind_48h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Zaun_48h.csv', 'Zaun_Wind_48h')
    Zaun_Wind_72h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Zaun_72h.csv', 'Zaun_Wind_72h')
    Zaun_Wind_96h = ErstelleForesterspeed('Daten/Trainingsdaten/Trainingsdaten_Zaun_96h.csv', 'Zaun_Wind_96h')


