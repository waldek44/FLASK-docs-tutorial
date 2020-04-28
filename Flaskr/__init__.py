import os

from flask import Flask


# create_app to funkcja fabryki aplikacji.
def create_app(test_config=None):
    # tworzę i konfiguruję aplikację (instancję Flask)

    # __name__ to nazwa bieżącego modułu Python. Aplikacja musi wiedzieć, gdzie się znajduje,
    # aby skonfigurować niektóre ścieżki, a __name__ to wygodny sposób, aby to powiedzieć.

    # instance_relative_config = True informuje aplikację, że pliki konfiguracyjne są względne względem folderu
    # instancji. Folder instancji znajduje się poza pakietem flaskr i może przechowywać lokalne dane,
    # które nie powinny być przypisane do kontroli wersji, takie jak klucze tajne konfiguracji i plik bazy danych.

    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_mapping () ustawia domyślną konfigurację, której będzie używać aplikacja

    # SECRET_KEY jest używany przez Flask i rozszerzenia do zapewnienia bezpieczeństwa danych. Jest ustawiony na „dev”,
    # aby zapewnić wygodną wartość podczas programowania, ale należy go zastąpić losową wartością podczas wdrażania.

    # DATABASE to ścieżka, w której zostanie zapisany plik bazy danych SQLite. Jest to ścieżka app.instance_path,
    # która jest ścieżką wybraną przez Flask dla folderu instancji.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # app.config.from_pyfile () przesłania domyślną konfigurację wartościami pobranymi z pliku config.py w
        # folderze instancji, jeśli istnieje.
        # Na przykład podczas wdrażania można go użyć do ustawienia prawdziwego klucza SECRET_KEY.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # test_config można również przekazać do fabryki i zostanie on użyty zamiast konfiguracji instancji.
        # Dzięki temu testy, można skonfigurować niezależnie od skonfigurowanych wartości programistycznych.
        app.config.from_mapping(test_config)

    # os.makedirs() zapewnia, że​ścieżka app.instance_path istnieje. Flask nie tworzy automatycznie folderu instancji,
    # ale należy go utworzyć, ponieważ Twój projekt utworzy tam plik bazy danych SQLite.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # prosta routa na start
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
