from flask import Flask, render_template, flash, redirect, url_for, request
from peewee import IntegrityError, fn

from models import English
from config import config

SECRET_KEY = config.SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

lst_main_menu = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'Добавить', 'url': '/add'},
    {'name': 'Обновить', 'url': '/update'},
    {'name': 'Удалить', 'url': '/delete'},
    {'name': 'Просмотр', 'url': '/show'},
]
 
@app.route('/')
def index():
    return render_template('index.html', title='Главная', lst_main_menu=lst_main_menu)


@app.route('/add')
def add():
    return render_template('add.html', title='Добавление', lst_main_menu=lst_main_menu)



@app.route('/add_word', methods=['POST'])
def input_data():
    if request.method == 'POST':
        word = request.form['word'].capitalize()
        translate = request.form['translate'].capitalize()
        try:
            if English.create(word=word, translate=translate):
                flash(f'Слово <b>{word}</b> и его перевод <b>{translate}</b> добавленны', category='sucess')
        except IntegrityError:
            flash(f'Слово <b>{word}</b> в базе существует')
        return render_template('add.html', lst_main_menu=lst_main_menu )
    else:
        return redirect(url_for('add_word'))


@app.route('/update')
def update():
    return render_template('update.html', title='Обновить', lst_main_menu=lst_main_menu)


@app.route('/delete')
def delete():
    return render_template('delete.html', title='Удаление', lst_main_menu=lst_main_menu)

@app.route('/show')
def show():
    count_words = len(English.select())
    return render_template('show.html', title='Просмотр', lst_main_menu=lst_main_menu,
                           count_words=count_words)


@app.route('/random_note')
def random_note():
    count_words = len(English.select())
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('random_note.html', random_query=one_obj, count_words=count_words,
                           lst_main_menu=lst_main_menu)


@app.route('/all_notes', methods=['get'])
def all_notes():
    querry_all = English.select()
    count_words = len(English.select())
    return render_template('all_notes.html', querry_all=querry_all, 
                           count_words=count_words, lst_main_menu=lst_main_menu)


@app.route('/count_notes', methods=['POST'])
def count_notes():
    if request.method == 'POST':
        count = request.form['count']
        query_count = English.select().limit(count)
    return render_template('count_notes.html', query_count=query_count, lst_main_menu=lst_main_menu)

if __name__ == '__main__':
    app.run(debug=config.FLASK_DEBUG)
