# scms2
Die Webseite der Schützenbruderschaft Oeventrop.

# Installation

Nach dem Klonen des Repositories die Abhängigkeiten installieren:

`pip install -r requirements.txt`

Für postgres noch psycopg2 installieren

`pip install psycopg2`

Die Datei

`scms2/settings/locale.py`

erstellen und mit Zugangsdaten für postgres füttern. Für lokalen Zugriff auf
eine Datenbank `scms2dev` sieht das so aus:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scms2dev',
    }
}
```

Außerdem in diese Datei noch einen `SECRET_KEY` einfügen. Man kann auch die
Beispiel-Datei `scms2/settings/local.py.example` einfach umbenennen.

Für die nächsten Teile in das verzeichnis `scms2` wechseln und die Datei
`manage.py` ausführbar machen. Ansonsten `python3 manage.py ...` verwenden.

Dann die Datenstruktur migrieren:

`./manage.py migrate`

und die Initialen Daten laden

`./manage.py load_initial_data`


Dann loslegen, Nutzer und Passwort sind:
- admin
- changeme
