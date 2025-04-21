from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="terms_db",
        user="postgres",
        password="kod1601370",
        host="localhost",
        port="5432"
    )

@app.route('/')
def index():
    letter = request.args.get("letter", "A")  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, term, definition FROM terms WHERE term ILIKE %s ORDER BY term", (letter + "%",))
    terms = cursor.fetchall()
    cursor.close()
    conn.close()

    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    return render_template("index.html", terms=terms, alphabet=alphabet)

# Добавление термина
@app.route('/add', methods=['POST'])
def add_term():
    term = request.form.get('term')
    definition = request.form.get('definition')

    if term and definition:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO terms (term, definition) VALUES (%s, %s)", (term, definition))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('index', letter=term[0].upper()))

# Удаление термина
@app.route('/delete/<int:term_id>', methods=['POST'])
def delete_term(term_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM terms WHERE id = %s", (term_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)