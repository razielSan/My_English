from flask import Flask, render_template, flash, redirect, url_for, request
from peewee import IntegrityError, fn

from models import English
from config import config

app = Flask(__name__)
app.config.from_object(__name__)

lst_main_menu = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'Добавить', 'url': '/add'},
    {'name': 'Обновить', 'url': '/update'},
    {'name': 'Удалить', 'url': '/delete'},
    {'name': 'Show', 'url': '/show'},
]
 
@app.route('/')
def index():
    return render_template('index.html', title='Главная', lst_main_menu=lst_main_menu)


@app.route('/add')
def add():
    return render_template('add.html', title='Добавление', lst_main_menu=lst_main_menu)



@app.route('/add_word', methods['POSTS'])
def input_data():
    if request.post == 'POST':
        word = request.form['word'].capitalize()
        translate = request.form['translate'].capitalize()
        try:
            if English.create(word=word, translate=translate):
                flash(f'Слово <b>{word}</b> и его перевод <b>{translate}</b> добавленны', category='sucess')
        except IntegrityError:
            flash(f'Слово <b>{word}</b> в базе существует')
        return render_template('add.html', lst_main_menu=lst_main_menu )


@app.route('/update')
def update():
    return render_template('update.html', title='Просмотр', lst_main_menu=lst_main_menu)


@app.route('/delete')
def delete():
    return render_template('delete.html', title='Удаление', lst_main_menu=lst_main_menu)

@app.route('/show')
def show():
    return render_template('show.html', title='Просмотр', lst_main_menu=lst_main_menu)


if __name__ == '__main__':
    app.run(debug=config.FLASK_DEBUG)
