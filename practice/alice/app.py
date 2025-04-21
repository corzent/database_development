from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    books = [
        {
            'title': "Alice's Adventures in Wonderland",
            'title_ru': "Алиса в стране чудес",
            'image': "alice.jpg",
            'author': "Lewis Carroll",
            'author_ru': "Льюис Кэрролл"
        }
    ]
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True) 