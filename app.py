import cgi
import json
# from requests import request # pip install --upgrade requests
from flask import Flask, request, jsonify
from db import DB
from db2 import DB2

# from flask_restx import Api, Resource, fields
# from flask_restplus import Api, Resource, fields
Data_Comms = None
app = Flask(__name__)  # creates an instance of the Flask class
Database = 'notes.db'


# isHttp = hasattr(request, 'method') and request.method in ['GET', 'POST', 'PUT', 'DELETE']
# if isHttp and 'User-Agent' in request and 'Postman' in request.headers.get('User-Agent'):
#     Database = 'workspace.db'  # Use workspace.db for requests from Postman
# else:
#     Database = 'notes.db'


def get_database(incoming_request: request):
    # Check the request headers
    condition = 'User-Agent' in incoming_request.headers and 'Postman' in incoming_request.headers.get('User-Agent')
    if condition:
        return 'workspace.db'  # Use workspace.db for requests from Postman

    else:
        return 'notes.db'


# Swagger Configurations
# pip install --upgrade werkzeug
# pip install --upgrade flask-restplus
# pip install --upgrade flask_restx
# pip install flask-restx
# /swagger
# api = Api(app, version='1.0', title='Notes_api_flask', description='distributed api that can be used'
#                                                                    'for a large commerce set-up')
# ns = api.namespace('items', description='Item operations')
# item_model = api.model('Item', {
#     'id': fields.Integer(readonly=True, description='The item identifier'),
#     'name': fields.String(required=True, description='The item name'),
# })


# @ns.route('/<int:id>')
# class Item(Resource):
#     @ns.marshal_with(item_model)
#     def get(self, id):
#         """Fetch an item by ID"""
#         pass


def init_db():
    db_name = get_database(request)
    db = DB(db_name)
    # DB.create_notes_table_if_not_exists()
    # with DB2.conn:
    #     DB2.create_notes_table_if_not_exists()


# sending get request and saving the response as response object
# r = requests.get(url = URL, params = PARAMS)

@app.route('/api/notes', methods=['POST'])
def create_note():
    # other method to get request body
    id_value = 0
    data = request.get_json()
    if data is None or 'content' not in data:
        return json.dumps({'error': 'Missing key: content'}), 422
    content_data = data["content"]
    if 'id' in data:
        id_value = data['id']
    # count = DB.get_total_notes_count()
    count = 0
    note_id = 1 if id_value == 0 or count == 0 else data["id"]
    new_note_id = DB2.create_note(content_data)

    return json.dumps({'message': 'Note created successfully', 'id': note_id}), 201
    # return jsonify({'message': 'Note created successfully'}), 201


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
    init_db()  # Initialize the database if the app is run directly and not from tests
    app.run(debug=True)
