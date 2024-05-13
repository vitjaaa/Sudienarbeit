@echo off

REM Name der virtuellen Umgebung
set venv_name=.venv

REM Name des Installationsverzeichnisses
set install_dir=%cd%\%venv_name%

REM Prüfen, ob Python vorhanden ist
where python > nul 2>&1
if %errorlevel% neq 0 (
    REM Python nicht gefunden, daher installieren
    echo Python wird installiert...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe
)

REM Prüfen, ob die virtuelle Umgebung bereits existiert
if not exist %venv_name% (
    REM Erstellen der virtuellen Umgebung
    python -m venv %venv_name%
)

REM Aktivieren der virtuellen Umgebung
call %venv_name%\Scripts\activate

REM Aktualisieren des Paketmanagers pip
python -m pip install --upgrade pip

REM Installieren der erforderlichen Pakete
python -m pip install -r requirements.txt

REM Entpacken der Datei Daten.zip
7z x Daten.zip

REM Deaktivieren der virtuellen Umgebung
deactivate

echo Installation abgeschlossen.
