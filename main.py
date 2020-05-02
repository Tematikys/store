from data import db_session, users, cart

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

import sqlite3
import io
import maps
import requests
import lxml.etree
import os


#шаблон авторизации

class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

#шаблон регистрации

class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')






#основной код

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

#получение информации из бд
connection = sqlite3.connect("db/1.db")
cur = connection.cursor()
categoriez = cur.execute("""SELECT * FROM Сategories""").fetchall()
itemz = cur.execute("""SELECT * FROM Items""").fetchall()
items = dict()
for category in categoriez:
    items[category[1]] = cur.execute("""SELECT * FROM Items WHERE Category IN (SELECT id FROM Categories WHERE Name = ?)""", (category[1],)).fetchall()
categories = []
for category in categoriez:
    categories.append([category[2], category[1]])

# Функция запуска
def main():
    
    port = int(os.environ.get("PORT", 6000))
    app.run(host='0.0.0.0', port=port)



    
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)

@app.route('/')
def root():
    return render_template('home.html', categories=categoriez)
@app.route('/my')
def my():
    connection_1 = sqlite3.connect("db/1.db")
    cur1 = connection_1.cursor()
    us = cur1.execute("""SELECT * FROM Users""").fetchall() 
    me = dict()
    for user in us:
        me[user[0]] = cur1.execute("""SELECT * FROM Carts WHERE user_id = ?""", (user[0],)).fetchall()
    return render_template('my.html', items=itemz, me=me[current_user.id], categories=categoriez)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/get/<p>/<pic>',  methods=['GET', 'POST'])
def get(p, pic):
    session = db_session.create_session()
    cart = session.query(cart.Cart).filter(cart.Cart.picture == pic, cart.Cart.user == current_user).first()
    if not cart:
        cart = cart.Cart()
        cart.picture = pic
        current_user.cart.append(cart)
        session.merge(current_user)
        session.commit()
    return redirect(f'/item/{p}/{pic}')

@app.route('/dell/<int:id>', methods=['GET', 'POST'])
@login_required
def dell(id):
    session = db_session.create_session()
    cart = session.query(cart.Cart).filter(Cart.Cart.id == id,
                                      cart.Cart.user == current_user).first()
    if cart:
        session.delete(cart)
        session.commit()
    else:
        abort(404)
    return redirect('/my')
     
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/home')
def gallery():
    return render_template('home.html',
                           categories=categoriez)

@app.route('/category/<p>')
def painter(p):
    return render_template('category.html', items=items[p], p=p)


@app.route('/item/<p>/<pic>')
def picture(p, pic):
    return render_template('item.html', items=items[p], p=pic, category=p)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)





if __name__ == '__main__':
    db_session.global_init("db/1.db")
    main()
