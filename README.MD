# FLASK Tutorial official PL
> https://flask.palletsprojects.com/en/1.1.x/tutorial/

### 1 Project Layout
Tworzę projekt w PyCharm. 

Instaluję Flask `pip install Flask`

Dodaję **.gitignore**
```
venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/

.idea/
```

### 2 Application Setup

> Aplikacja Flask jest instancją klasy **Flask**.  
>Wszystko związane z aplikacją, takie jak konfiguracja i adresy URL, 
> zostanie zarejestrowane w tej klasie.  
>
> Najprostszym sposobem na utworzenie aplikacji Flask jest utworzenie globalnej instancji **Flask** 
>bezpośrednio u góry kodu. Chociaż jest to proste i przydatne w niektórych przypadkach, może powodować pewne 
>trudne problemy w miarę rozwoju projektu.  
>
> Zamiast globalnie tworzyć instancję Flask, utworzysz ją wewnątrz funkcji. Ta funkcja jest znana jako fabryka aplikacji.    
> Każda konfiguracja, rejestracja i inne ustawienia wymagane przez aplikację będą miały miejsce wewnątrz funkcji, 
> a następnie aplikacja zostanie zwrócona.

1. Tworzę folder Flaskr `mkdir Flaskr`

2. Tworzę plik **__init__.py** 
> **__init__.py** ma dwa obowiązkowi: będzie zawierać fabrykę aplikacji i mówi Pythonowi, że katalog flaskr 
> powinien być traktowany jako pakiet.
 
3. Uruchamiam aplikację.
Najpierw mówię Flaskowi gdzie ma znaleźć moją aplikację
```
set FLASK_APP=flaskr
```

Tryb **development** pokazuje interaktywny debugger za każdym razem, gdy strona zgłosi wyjątek, i uruchamia ponownie 
serwer za każdym razem, gdy wprowadzasz zmiany w kodzie.
```
set FLASK_ENV=development
```

I Boom!
```
flask run
```

### 3 Define and Access the Database
> Pierwszą rzeczą do zrobienia podczas pracy z bazą danych jest utworzenie połączenia z nią. 
> Wszelkie zapytania i operacje są wykonywane przy użyciu połączenia, które jest zamykane po zakończeniu pracy.
> W aplikacjach internetowych to połączenie jest zazwyczaj powiązane z żądaniem. Jest on tworzony w pewnym momencie 
> podczas obsługi żądania i zamykany przed wysłaniem odpowiedzi.

1. W katalogu Flaskr tworzę plik **db.py**

2. Tworzę plik schema.sql

3. Importuję i wywołuję funkcję `def init_app(app)` z pliku **db.py** w **__init__.py** jako dolny import
funkcji fabryki **create_app**. 

```
# flaskr/__init__.py

    from . import db
    db.init_app(app)

```

4. W terminalu inicjuję `flask init-db` - w folderze **instance** mam teraz plik db sqlite3
