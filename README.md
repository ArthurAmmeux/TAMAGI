# TAMAGI
A tool to monitor space weather

## How to install TAMAGI

Prerequisite: Have a recent python distribution (>3.9)

1 - Go to the Tamagi Github: https://github.com/ArthurAmmeux/TAMAGI and download the “webapp” folder

2 - Install all necessary python packages using pip using the command:
$ pip install importlib jupyter ipyvuetify ipywidgets datetime os glob matplotlib seaborn opencv-python gzip shutdown zipfile tarfile numpy urllib pandas requests cairosvg json geopandas re io shapely

3 - Install voila: $ pip install voila in the command

4 - Run the command: $ voila ./Tamagi_webapp.ipynb

Your browser should open with the TAMAGI application



GNSS.ipynb : notebook qui a permis de rédiger le code de l'indice GNSS, avec des fonctions intermédiaires, beaucoup de commentaires
GNSS_implementation.ipynb : notebook ou l'on a gardé que les fonctions essentielles pour la GUI afin de simplifier la tâche d'implémentation
