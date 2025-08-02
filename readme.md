pyinstaller --onefile --windowed timer.py


pyinstaller --onefile --windowed --add-data "icon.ico;." --add-data "links.txt:."  --icon=icon.ico your_script.py

pyinstaller --add-data "links.txt:." timer.py 



