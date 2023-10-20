from flask import Flask
import sqlite3
from contextlib import closing
import json
from requests import request
from db import DB

app = Flask(__name__)
DATABASE = 'notes.db'  # Define DATABASE before calling init_db()


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
    # noinspection PyUnresolvedReferences
    data = request.get_json(force=True)
    if 'content' not in data:
        return json.dumps({'error': 'Missing key: content'}), 422

    # Call the DB.create_note method to create a new note
    new_note_id = DB.create_note(data['content'])

    return json.dumps({'message': 'Note created successfully', 'id': new_note_id}), 201


@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    # Call the DB.select_all_notes method to get all notes
    notes = [{'id': row['id'], 'content': row['content']} for row in DB.select_all_notes()]

    return json.dumps(notes), 200


@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    # Call the DB.select_one_note method to get a specific note
    note = DB.select_one_note(note_id)

    if not note:
        return json.dumps({'error': 'Note not found'}), 404

    return json.dumps({'id': note['id'], 'content': note['content']}), 200


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    # noinspection PyUnresolvedReferences
    data = request.get_json(force=True)
    if 'content' not in data:
        return json.dumps({'error': 'Missing key: content'}), 422

    # Call the DB.update_note method to update the note
    updated_rows = DB.update_note(note_id, data['content'])

    if updated_rows == 0:
        return json.dumps({'error': 'Note not found'}), 404

    return json.dumps({'message': 'Note updated successfully'}), 200


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    deleted_rows = DB.delete_note(note_id)
    if deleted_rows == 0:
        # If no rows were deleted, it means the note doesn't exist
        return json.dumps({'error': 'Note not found'}), 404
    else:
        return json.dumps({'message': 'Note deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
