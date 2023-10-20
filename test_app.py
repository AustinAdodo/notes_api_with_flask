import json
import unittest
from app import app, init_db
from db import DB
import sqlite3


class TestCase(unittest.TestCase):
    client = None

    def create_test_database(self):
        conn = sqlite3.connect(':memory:')
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        return conn

    @classmethod
    def setUpClass(cls):
        # cls.app = app.test_client()
        # cls.test_db = cls.create_test_database()
        cls.client.testing = True

    def setUp(self):
        DB.create_notes_table_if_not_exists()

    def tearDown(self):
        DB.drop_notes_table_if_exists()

    def test_post(self):
        "POST /api/notes 201"
        response = TestCase.client.post(
            "/api/notes",
            json={"content": "hello"},
        )
        self.assertEqual(response.status_code, 201)

    def test_get(self):
        "GET /api/notes/id 200"
        response = TestCase.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        self.assertEqual(response.status_code, 201)
        response = TestCase.client.get("/api/notes/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data()),
            {"content": "hello again", "id": 1}
        )

    def test_no_content(self):
        """GET /api/notes/id 404"""
        response = TestCase.client.get("/api/notes/2", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """DELETE /api/notes/id 200"""
        response = TestCase.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        self.assertEqual(response.status_code, 201)
        response = TestCase.client.delete("/api/notes/1")
        self.assertEqual(response.status_code, 200)
        response = TestCase.client.get("/api/notes/1")
        self.assertEqual(response.status_code, 404)

    def test_put_200(self):
        """PUT /api/notes/id 200"""
        response = TestCase.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        self.assertEqual(response.status_code, 201)
        response = TestCase.client.put(
            "/api/notes/1",
            json={"content": "hello again!"},
        )
        self.assertEqual(response.status_code, 200)
        response = TestCase.client.get("/api/notes/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data()),
            {"content": "hello again!", "id": 1}
        )

    def test_put_422(self):
        """PUT /api/notes/id 422"""
        response = TestCase.client.put("/api/notes/1", json={})
        self.assertEqual(response.status_code, 422)

    def test_put_404(self):
        """PUT /api/notes/id 404"""
        response = TestCase.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        self.assertEqual(response.status_code, 201)
        response = TestCase.client.put(
            "/api/notes/2",
            json={"content": "hello again!"},
        )
        self.assertEqual(response.status_code, 404)
