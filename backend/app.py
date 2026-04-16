from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Connessione database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Creazione tabella (solo la prima volta)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prenotazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            orario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# GET tutte le prenotazioni
@app.route('/prenotazioni', methods=['GET'])
def get_prenotazioni():
    conn = get_db_connection()
    prenotazioni = conn.execute('SELECT * FROM prenotazioni').fetchall()
    conn.close()
    return jsonify([dict(row) for row in prenotazioni])

# POST nuova prenotazione
@app.route('/prenotazioni', methods=['POST'])
def add_prenotazione():
    data = request.json
    nome = data['nome']
    data_visita = data['data']
    orario = data['orario']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO prenotazioni (nome, data, orario) VALUES (?, ?, ?)',
        (nome, data_visita, orario)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione aggiunta"}), 201

# DELETE prenotazione
@app.route('/prenotazioni/<int:id>', methods=['DELETE'])
def delete_prenotazione(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM prenotazioni WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Prenotazione eliminata"})

if __name__ == '__main__':
    app.run(debug=True)
