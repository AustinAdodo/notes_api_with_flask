from flask import Flask
import json
from requests import request
from db import DB

app = Flask(__name__)
DATABASE = 'notes.db'


def init_db():
    with DB.conn:
        DB.create_notes_table_if_not_exists()


@app.route('/api/notes', methods=['POST'])
def create_note():
    # data = request.get_json()
    data = None
    try:
        data = request().json()
    except json.JSONDecodeError as e:
        print('Error parsing JSON data: {}'.format(e))
    if data is None or 'content' not in data:
        return json.dumps({'error': 'Missing key: content'}), 422

    new_note_id = DB.create_note(data['content'])

    return json.dumps({'message': 'Note created successfully', 'id': new_note_id}), 201


@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    notes = [{'id': row['id'], 'content': row['content']} for row in DB.select_all_notes()]

    return json.dumps(notes), 200


@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
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

    updated_rows = DB.update_note(note_id, data['content'])

    if updated_rows == 0:
        return json.dumps({'error': 'Note not found'}), 404

    return json.dumps({'message': 'Note updated successfully'}), 200


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    deleted_rows = DB.delete_note(note_id)
    if deleted_rows == 0:
        return json.dumps({'error': 'Note not found'}), 404
    else:
        return json.dumps({'message': 'Note deleted successfully'}), 200


if __name__ == '__main__':
    init_db()  # Initialize the database if the app is run directly and not from tests
    app.run(debug=True)
