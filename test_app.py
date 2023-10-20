import json
import unittest
from app import app


# from db import DB


class TestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True  # Set the app to testing mode
        cls.client = app.test_client()
        # You don't need to create a test database for the Flask client
        # Testing will use a separate in-memory database by default

    def setUp(self):
        pass

        # DB.create_notes_table_if_not_exists()
        # No need to create the notes table here, it's done in app.py when the app is started

    def test_post(self):
        "POST /api/notes 201"
        response = self.client.post(
            "/api/notes",
            json={"content": "hello"},
        )
        self.assertEqual(response.status_code, 201)

    def test_get(self):
        "GET /api/notes/id 200"
        self.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        response = self.client.get("/api/notes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data(as_text=True)),
            {"content": "hello again", "id": 1}
        )

    def test_no_content(self):
        """GET /api/notes/id 404"""
        response = self.client.get("/api/notes/2")
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """DELETE /api/notes/id 200"""
        self.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        response = self.client.delete("/api/notes/1")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/notes/1")
        self.assertEqual(response.status_code, 404)

    def test_put_200(self):
        """PUT /api/notes/id 200"""
        self.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        response = self.client.put(
            "/api/notes/1",
            json={"content": "hello again!"},
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/notes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data(as_text=True)),
            {"content": "hello again!", "id": 1}
        )

    def test_put_422(self):
        """PUT /api/notes/id 422"""
        response = self.client.put("/api/notes/1", json={})
        self.assertEqual(response.status_code, 422)

    def test_put_404(self):
        """PUT /api/notes/id 404"""
        self.client.post(
            "/api/notes",
            json={"content": "hello again"},
        )
        response = self.client.put(
            "/api/notes/2",
            json={"content": "hello again!"},
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
