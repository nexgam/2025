from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'messages.db'

# Initialisation de la base de données
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour créer un message personnalisé
@app.route('/create', methods=['GET', 'POST'])
def create_message():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
            conn.commit()
            message_id = cursor.lastrowid
        return redirect(url_for('personalized_message', message_id=message_id))
    return render_template('create_message.html')

# Route pour afficher un message personnalisé
@app.route('/message/<int:message_id>')
def personalized_message(message_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, message FROM messages WHERE id = ?', (message_id,))
        result = cursor.fetchone()
    if result:
        name, message = result
        return render_template('personalized_message.html', name=name, message=message, message_id=message_id)
    else:
        return "Message non trouvé.", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)