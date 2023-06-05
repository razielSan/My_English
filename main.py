from flask import Flask, render_template, flash, redirect, url_for, request
from peewee import IntegrityError, fn

from models import English
from config import config

SECRET_KEY = config.SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

 
@app.route('/')
def index():
    count_words = len(English.select())
    return render_template('index.html', count_words=count_words)


@app.route('/add_page', methods=['get'])
def add():
    count_words = len(English.select())
    return render_template('add.html', count_words=count_words)



@app.route('/add', methods=['POST', 'GET    '])
def input_data():
    if request.method == 'POST':
        word = request.form['word'].capitalize()
        translate = request.form['translate'].capitalize()
        try:
            if English.create(word=word, translate=translate):
                flash(f'Слово <b>{word}</b> и его перевод <b>{translate}</b> добавленны', category='success')
        except IntegrityError:
            flash(f'Слово <b>{word}</b> в базе существует', category='error')
        return render_template('add.html')
    else:
        return redirect(url_for('add_page'))


@app.route('/update_page')
def update():
    count_words = len(English.select())
    return render_template('update.html', count_words=count_words)


@app.route('/update', methods=['POST', 'GET'])
def update_data():
    if request.method == 'POST':
        words = request.form['word'].capitalize()
        if English.select().where(English.word==words):
            words_upd = request.form['translate']
            query = English.update(translate=words_upd).where(English.word == words)
            query.execute()
            flash(f'Слово <b>{words}</b>, было обновленно на  <b>{words_upd}</b>', category='attention')
        else:
            flash(f'Слово <b>{words}</b> не найденно в базе', category='error')
        return render_template('update.html')
    else:
        return redirect(url_for('update_page'))


@app.route('/delete_page')
def delete():
    count_words = len(English.select())
    return render_template('delete.html')


@app.route('/delete', methods=['post', 'get'])
def delete_data():
    if request.method == 'POST':
        word = request.form['word'].capitalize()
        del_word = English.select().where(English.word==word)
        if del_word:
            English.delete_by_id(del_word)
            flash(f'Слово {word} было удаленно', category='success')
        else:
            flash(f'Слово {word} в базе не найденно', category='error')
        
    return render_template('delete.html')


@app.route('/show')
def show():
    count_words = len(English.select())
    return render_template('show.html', count_words=count_words)


@app.route('/random_note')
def random_note():
    count_words = len(English.select())
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('random_note.html', random_query=one_obj, count_words=count_words)


@app.route('/all_notes', methods=['get'])
def all_notes():
    querry_all = English.select()
    count_words = len(English.select())
    return render_template('all_notes.html', querry_all=querry_all, 
                           count_words=count_words)


@app.route('/count_notes', methods=['POST'])
def count_notes():
    if request.method == 'POST':
        count = request.form['count']
        query_count = English.select().limit(count)
    return render_template('count_notes.html', query_count=query_count)

if __name__ == '__main__':
    app.run(debug=config.FLASK_DEBUG)
