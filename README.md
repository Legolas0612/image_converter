# HEIC Converter

Ein einfaches Tool zum **Konvertieren von HEIC-Bildern** in JPEG oder PNG auf Windows.  
Die App unterstützt **Ordner mit vielen Bildern**, behält die **Ordnerstruktur** bei und zeigt **Bildanzahl, geschätzte Dateigröße, Geschwindigkeit und ETA** an.

---

## Features

- Drag & Drop von Quellordnern
- Automatische Zielordner-Erstellung (`<Quellordner>_converted`)
- Konvertierung nur von **HEIC-Dateien**; andere Formate werden unverändert kopiert
- Auswahl zwischen **JPEG** und **PNG**
- Einstellbare **JPEG-Qualität** (mit Anzeige: niedrig = kleiner Speicher, hoch = größerer Speicher)
- Fortschrittsanzeige mit **geschätzter Gesamtgröße**, **Bilder pro Sekunde** und **ETA**
- Große, übersichtliche Benutzeroberfläche

---

## Installation

1. Python 3.11+ installieren  
2. Projekt klonen oder entpacken  
3. Virtuelle Umgebung erstellen:

```bash
python -m venv venv
venv\Scripts\activate

    Abhängigkeiten installieren:

pip install -r requirements.txt

Nutzung

    app.py starten:

python app.py

    Quellordner per Drag & Drop oder über den „Durchsuchen…“-Button auswählen

    Zielordner wird automatisch vorgeschlagen (Quellordner_converted)

    Format und Qualität einstellen

    Auf „Conversion starten“ klicken

    Hinweis: HEIC-Dateien werden konvertiert, andere Dateien bleiben unverändert.

Testdaten

Für Stress-Tests können große Mengen HEIC-Bilder generiert werden:

python generate_heic_dataset.py

    Achtung: Der Ordner kann mehrere GB groß werden.
    Nicht auf GitHub hochladen! Dafür gibt es .gitignore.

Hinweise

    Windows-only (Tkinter + pillow-heif)

    Keine Upscaling-Funktion – Bilder behalten ihre Originalgröße

    Optimiert für große Datenmengen, kann mehrere Kerne verwenden

.gitignore

Alle Bilder und große Testordner werden ignoriert:

# Bilder
*.jpg
*.jpeg
*.png
*.heic
*.gif
*.bmp
*.tiff
*.webp

# Testordner
heic_test_data/
images/
output/

# Python temporäre Dateien
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE / Editor
.vscode/
*.idea/
*.sublime-project
*.sublime-workspace

# Betriebssystem spezifisch
.DS_Store
Thumbs.db

Lizenz

Dieses Projekt ist frei nutzbar. Änderungen und Verbesserungen sind willkommen.