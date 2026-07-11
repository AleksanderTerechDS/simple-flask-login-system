from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, Field, ValidationError

app = Flask(__name__)
app.secret_key = 'klucz_do_sesji_www'

engine = create_engine('sqlite:///uzytkownicy.db', connect_args={"check_same_thread": False})
Base = declarative_base()


class UserBaza(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    haslo = Column(String, nullable=False)


class ZdjecieBaza(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    opis = Column(String, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def zainicjalizuj_zdjecia():
    if session.query(ZdjecieBaza).count() == 0:
        baza_linkow = [
            {
                "url": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSDItRB0IZ2c1PfPwnzgOLXI4rNGKzu4B9V8ed2y-3fNJALyvMvWqsAx9u34gUox_I9w1pXtF2mJOlfNg4",
                "opis": "Gory"},
            {
                "url": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcRRarfh4WSA6-2H2ylrOOkE0jYJxvCD8Pe8LeSDnVF5Gw8xR9XjIWNTTtZ8B13Z4LPBTFxHctdDLH1qEzo",
                "opis": "Ocean"},
            {
                "url": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcS-C7dBI-y9yQVCDPrFfOFWYpDdjtYTj0chZuffVFYvrCtAoy12YxCwVZjgYbWKLs3EtAtkStqUZL1sWAg",
                "opis": "Las"},
            {
                "url": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcQpVLqRKRnp3KBOS0riQ6ob5UyT30PehufQhwPUc86D_MGWWW9JOvpBL4lwSjaSWsSTlvu6HJXcXSfepgs",
                "opis": "Cyberpunk"},
            {
                "url": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSU1QOyJ8Qtcz2KSiYei8gOb_Fu2FtycLoOxStnTszWBN0XV4CT8-ooGEEtb-w2V0mZuWVDXHSSrwYjWWA",
                "opis": "Pustynia"},
            {
                "url": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcTiENJdKIHy8GIambEHJmV7QJ1I7duBIgFLmACvaC1UXxySfr_oaObXrMXlvSZ-kGHMKGNpTktnIuSg98Y",
                "opis": "Czerwona Panda"},
            {
                "url": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcT_kvLagVjg2jTKzjtklEVxE_cqg_bMSGLtHqh6tZgKI5_Oc6DEExKG-w6uK0rDh_q7-tAJ1N03VYTMO8Q",
                "opis": "Wodospad"},
            {
                "url": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcRiC9W45zc8cIhPeQV8iyNfZg_8ElHITk9noFccyQiLaO6N70mlFZwYykIMr2TqSQCLsfUu54WIXwaB6sU",
                "opis": "Zamek"},
            {
                "url": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcS_6-hjVacGASCFwnQdDTFtiByd_8Mil1aNOhGjxbK9sqSq511Ri86crIj57SXvWdQA-vVyYfYreMNTg20",
                "opis": "Kosmos"},
            {
                "url": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRTP1gvgPttsJICIwF6EJL5axcPEoZfdAEfBkohhZzXLRPbHlRplbdcoUU5iwKxiwv_oQZ1AmYNULXfYCE",
                "opis": "Plaza"}
        ]
        for z in baza_linkow:
            session.add(ZdjecieBaza(url=z["url"], opis=z["opis"]))
        session.commit()


zainicjalizuj_zdjecia()


class UserFormularz(BaseModel):
    login: str = Field(min_length=3, max_length=20)
    haslo: str = Field(min_length=4)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        dane_z_formularza = request.form.to_dict()
        try:
            valid_data = UserFormularz(**dane_z_formularza)
            istnieje = session.query(UserBaza).filter_by(login=valid_data.login).first()
            if istnieje:
                return "Ten login jest juz zajety! Sprobuj innego."

            nowy_user = UserBaza(login=valid_data.login, haslo=valid_data.haslo)
            session.add(nowy_user)
            session.commit()
            return f"Rejestracja udana! <a href='/login'>Zaloguj sie</a>"
        except ValidationError as e:
            return f"Blad walidacji: {e.errors()[0]['msg']}"
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        wpisany_login = request.form.get('login')
        wpisane_haslo = request.form.get('haslo')

        user = session.query(UserBaza).filter_by(login=wpisany_login).first()
        if user and user.haslo == wpisane_haslo:
            flask_session['user_login'] = user.login
            return redirect(url_for('dashboard'))
        else:
            return "Bledne dane logowania! <a href='/login'>Sprobuj ponownie</a>"
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_login' not in flask_session:
        return redirect(url_for('login'))

    losowe_zdjecie = session.query(ZdjecieBaza).order_by(func.random()).first()
    return render_template('dashboard.html', login=flask_session['user_login'], zdjecie=losowe_zdjecie)


@app.route('/logout')
def logout():
    flask_session.pop('user_login', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)