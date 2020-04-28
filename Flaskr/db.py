import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# g to specjalny obiekt, który jest unikalny dla każdego żądania.
# Służy do przechowywania danych, do których dostęp może mieć wiele funkcji podczas żądania.
# Połączenie zostanie zapisane i ponownie użyte zamiast tworzenia nowego połączenia,
# jeśli get_db zostanie wywołane po raz drugi w tym samym żądaniu.

def get_db():
    if 'db' not in g:

        # Funkcja sqlite3.connect () ustanawia połączenie z plikiem wskazywanym przez klucz konfiguracyjny DATABASE.
        # Ten plik nie musi jeszcze istnieć i będzie dostępny do momentu zainicjowania bazy danych później.

        g.db = sqlite3.connect(

            # current_app to kolejny obiekt specjalny, który wskazuje aplikację Flask obsługującą żądanie.
            # Ponieważ korzystałeś z fabryki aplikacji, nie ma obiektu aplikacji podczas pisania reszty kodu.

            # get_db zostanie wywołany, gdy aplikacja zostanie utworzona i obsługuje żądanie,
            # więc można użyć current_app.

            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # sqlite3.Row informuje połączenie, aby zwracało wiersze, które zachowują się jak słowniki.
        # Umożliwia to dostęp do kolumn według nazwy.
        g.db.row_factory = sqlite3.Row

    return g.db


# close_db sprawdza, czy połączenie zostało utworzone, sprawdzając, czy ustawiono g.db. Jeśli połączenie istnieje,
# jest zamknięte. W dalszej części powiesz aplikacji o funkcji close_db w fabryce aplikacji,
# aby była wywoływana po każdym żądaniu.

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# funkcje Python, które będą uruchamiać polecenia SQL
def init_db():

    # get_db zwraca połączenie z bazą danych, które służy do wykonywania poleceń odczytanych z pliku.
    db = get_db()

    # open_resource () otwiera plik w stosunku do pakietu flaskr, co jest przydatne, ponieważ niekoniecznie będziesz
    # wiedział, gdzie jest ta lokalizacja podczas późniejszego wdrażania aplikacji.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# click.command () definiuje polecenie wiersza poleceń o nazwie init-db, które wywołuje funkcję init_db
# i wyświetla użytkownikowi komunikat o powodzeniu.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# Funkcje close_db i init_db_command muszą być zarejestrowane w instancji aplikacji;
# w przeciwnym razie aplikacja nie będzie z nich korzystać.

# dlatego tworzę funkcję która pobiera aplikację i dokonuje rejestracji.
def init_app(app):

    # app.teardown_appcontext() każe Flaskowi wywołać tę funkcję podczas czyszczenia po zwróceniu odpowiedzi.
    app.teardown_appcontext(close_db)
    # app.cli.add_command () dodaje nowe polecenie, które można wywołać za pomocą polecenia flask.
    app.cli.add_command(init_db_command)