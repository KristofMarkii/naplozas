import PyInstaller.__main__
import os

# A fájl elérési útvonala
script_path = os.path.join("naplo_app", "main.py")

PyInstaller.__main__.run([
    script_path,
    '--name=NaploApp',
    '--onefile',
    '--windowed',
    '--add-data=naplo_app/main.py;naplo_app',
    '--icon=naplo_icon.ico',  # Ha van ikonod, akkor add meg itt
    '--hidden-import=streamlit',
    '--hidden-import=pandas',
    '--hidden-import=plotly',
])