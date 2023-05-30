from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    name = 'Lera'
    return f"Hello {name}"


if __name__ == '__main__':
    app.run(debug=1)

