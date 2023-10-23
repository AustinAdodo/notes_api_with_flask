import sqlite3
from flask import request


class DB:
    def __init__(self):
        user_agent = request.headers.get('User-Agent')
        self.path = 'workspace.db' if 'Postman' in user_agent else 'notes.db'
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_notes_table_if_not_exists(self):
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        );
        """
        try:
            self.cursor.executescript(query)
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {str(e)}")

    def drop_notes_table_if_exists(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS notes;")
            self.conn.commit()
        except Exception as e:
            print(f"Error dropping table: {str(e)}")

    def create_note(self, contents):
        query = "INSERT INTO notes (content) VALUES (?);"
        try:
            self.cursor.execute(query, (contents,))
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            (print(f"Error creating note: {str(e)}"))
        return None

    def update_note(self, note_id, content):
        query = "UPDATE notes SET content=? WHERE id=?;"
        try:
            self.cursor.execute(query, (content, note_id))
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Error updating note: {str(e)}")
            return -1

    def delete_note(self, note_id):
        query = "DELETE FROM notes WHERE id=?;"
        try:
            self.cursor.execute(query, (note_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Error deleting note: {str(e)}")
            return -1

    def select_one_note(self, note_id):
        query = "SELECT * FROM notes WHERE id=?;"
        try:
            self.cursor.execute(query, (note_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error selecting one note: {str(e)}")
            return None

    def select_all_notes(self):
        try:
            self.cursor.execute("SELECT * FROM notes;")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error selecting all notes: {str(e)}")
            return None

    def get_total_notes_count(self):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                query = "SELECT COUNT(*) FROM notes;"
                cursor.execute(query)
                result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
        except Exception as e:
            print(f"Error getting total notes count: {str(e)}")
            return 0
