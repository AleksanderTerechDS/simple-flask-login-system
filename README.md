# Flask User Authentication System

Minimalistyczny system rejestracji i logowania użytkowników w architekturze Full-Stack. Projekt demonstruje bezpieczny przepływ danych (Data Flow) od formularza HTML, przez walidację reguł biznesowych, aż po trwały zapis w bazie danych.

Po zalogowaniu użytkownik uzyskuje dostęp do chronionego panelu deweloperskiego (Dashboard) z funkcją losowania unikalnych obrazków z bazy danych.

## Architektura i Przepływ Danych

Aplikacja została zbudowana w oparciu o trzy niezależne warstwy backendowe:

1. **Flask (Warstwa Prezentacji i Routingu):** Przechwytuje żądania HTTP (GET/POST), zarządza sesją użytkownika (`flask.session`) oraz renderuje dynamiczne szablony HTML przy użyciu silnika Jinja2.
2. **Pydantic (Warstwa Walidacji):** Działa jako strażnik aplikacji (Guard). Surowe dane z formularzy są mapowane na model Pydantica, który rygorystycznie sprawdza typy oraz reguły biznesowe (np. minimalna i maksymalna długość znaków) przed dopuszczeniem ich do bazy.
3. **SQLAlchemy + SQLite (Warstwa Danych):** Potężny ORM mapujący obiekty Pythona na relacyjną bazę danych SQLite. Zapewnia trwałość danych użytkowników oraz zarządza bazą obrazków.

## Użyte "Technologie"

* **Backend:** Python 3, Flask
* **Walidacja danych:** Pydantic (v2)
* **Baza danych & ORM:** SQLAlchemy, SQLite
* **Frontend:** HTML5, Modern CSS (Flexbox, CSS Variables, Dark Mode aesthetic)

## Struktura Projektu

```text
├── app.py                 # Główny plik backendu (Konfiguracja bazy, Pydantic, Trasy Flaska)
├── uzytkownicy.db         # Lokalna baza danych SQLite (tworzona automatycznie)
└── templates/             # Szablony stron WWW
    ├── index.html         # Strona główna
    ├── register.html      # Formularz tworzenia konta
    ├── login.html         # Formularz logowania
    └── dashboard.html     # Panel zalogowanego użytkownika (z losowaniem zdjęć)
