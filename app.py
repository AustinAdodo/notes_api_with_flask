from flask import Flask

# from flask import Flask, jsonify, request
import sqlite3
from contextlib import closing
from db import DB


# Helper function to initialize the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect(DATABASE)


init_db()


@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    if 'content' not in data:
        return jsonify({'error': 'Missing key: content'}), 422

    with closing(connect_db()) as db:
        cur = db.cursor()
        cur.execute("INSERT INTO notes (content) VALUES (?)", [data['content']])
        db.commit()

    return jsonify({'message': 'Note created successfully'}), 201


@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    with closing(connect_db()) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM notes")
        notes = [{'id': row[0], 'content': row[1]} for row in cur.fetchall()]

    return jsonify(notes), 200


# Endpoint to get a specific note
@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    with closing(connect_db()) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM notes WHERE id = ?", [note_id])
        note = cur.fetchone()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({'id': note[0], 'content': note[1]}), 200


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.json
    if 'content' not in data:
        return jsonify({'error': 'Missing key: content'}), 422

    with closing(connect_db()) as db:
        cur = db.cursor()
        cur.execute("UPDATE notes SET content = ? WHERE id = ?", [data['content'], note_id])
        db.commit()

    return jsonify({'message': 'Note updated successfully'}), 200


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    with closing(connect_db()) as db:
        cur = db.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", [note_id])
        db.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200


app = Flask(__name__)
DATABASE = 'notes.db'

if __name__ == '__main__':
    app.run(debug=True)
