# import cgi
import json
# from requests import request # pip install --upgrade requests
# from urllib.parse import parse_qs
# from werkzeug.wrappers import Request
from flask import Flask, jsonify, request
from db import DB
from db2 import DB2

app = Flask(__name__)  # creates an instance of the Flask class


def get_database_info():
    user_agent = request.headers.get('User-Agent')
    return 'workspace.db' if 'Postman' in user_agent else 'notes.db'


def init():
    # DB.create_notes_table_if_not_exists()
    with DB2.conn:
        DB2.create_notes_table_if_not_exists()


@app.route('/api/notes', methods=['POST'])
def create_note():
    # data = req.args.get('content')
    data = request.get_json()
    if data is None or 'content' not in data:
        return jsonify({'error': 'Missing key: content'}), 422
    database = get_database_info()
    db = DB() if database == 'workspace.db' else DB2()
    new_note_id = db.create_note(data['content'])
    db.close_connection()
    return jsonify({'message': 'Note created successfully', 'id': new_note_id}), 201


@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    notes = [{'id': row['id'], 'content': row['content']} for row in DB2.select_all_notes()]
    return json.dumps(notes), 200


@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = DB2.select_one_note(note_id)

    if not note:
        return json.dumps({'error': 'Note not found'}), 404

    return json.dumps({'id': note['id'], 'content': note['content']}), 200


@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    # #noinspection PyUnresolvedReferences
    data = request.get_json(force=True)
    if 'content' not in data:
        return json.dumps({'error': 'Missing key: content'}), 422

    updated_rows = DB2.update_note(note_id, data['content'])

    if updated_rows == 0:
        return json.dumps({'error': 'Note not found'}), 404

    return json.dumps({'message': 'Note updated successfully'}), 200


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    deleted_rows = DB2.delete_note(note_id)
    if deleted_rows == 0:
        return json.dumps({'error': 'Note not found'}), 404
    else:
        return json.dumps({'message': 'Note deleted successfully'}), 200


if __name__ == '__main__':
    init()  # Initialize the database if the app is run directly and not from tests
    app.run(debug=True)
