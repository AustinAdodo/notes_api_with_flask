# path = "./workspace.db"
# conn = sqlite3.connect(path, check_same_thread=False)
# conn.row_factory = sqlite3.Row
# cursor = conn.cursor()

import sqlite3


class DB:
    conn = None
    cursor = None

    def __init__(self, db_name):
        self.path = db_name
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    @classmethod
    def create_notes_table_if_not_exists(cls):
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        );
        """
        try:
            cls.cursor.executescript(query)
            cls.conn.commit()
        except Exception as e:
            print(f"Error creating table: {str(e)}")

    @classmethod
    def drop_notes_table_if_exists(cls):
        try:
            cls.cursor.execute("DROP TABLE IF EXISTS notes;")
            cls.conn.commit()
        except Exception as e:
            print(f"Error dropping table: {str(e)}")

    @classmethod
    def create_note(cls, contents):
        query = "INSERT INTO notes (content) VALUES (?);"
        try:
            with DB.conn:
                DB.cursor.execute(query, (contents,))
            return DB.cursor.lastrowid
        except sqlite3.Error as e:
            # Handle the exception, e.g., log the error, return an error response, etc.
            return None

    @classmethod
    def update_note(cls, note_id, content):
        query = "UPDATE notes SET content=? WHERE id=?;"
        try:
            cls.cursor.execute(query, (content, note_id))
            cls.conn.commit()
            return cls.cursor.rowcount
        except Exception as e:
            print(f"Error updating note: {str(e)}")
            return -1  # Or raise a custom exception or return an error response.

    @classmethod
    def delete_note(cls, note_id):
        query = "DELETE FROM notes WHERE id=?;"
        try:
            cls.cursor.execute(query, (note_id,))
            cls.conn.commit()
            return cls.cursor.rowcount
        except Exception as e:
            print(f"Error deleting note: {str(e)}")
            return -1  # Or raise a custom exception or return an error response.

    @classmethod
    def select_one_note(cls, note_id):
        query = "SELECT * FROM notes WHERE id=?;"
        try:
            cls.cursor.execute(query, (note_id,))
            return cls.cursor.fetchone()
        except Exception as e:
            print(f"Error selecting one note: {str(e)}")
            return None  # Or raise a custom exception or return an error response.

    @classmethod
    def select_all_notes(cls):
        try:
            cls.cursor.execute("SELECT * FROM notes;")
            return cls.cursor.fetchall()
        except Exception as e:
            print(f"Error selecting all notes: {str(e)}")
            return None  # Or raise a custom exception or return an error response.

    @classmethod
    def get_total_notes_count(cls):
        try:
            with cls.conn:
                cursor = cls.conn.cursor()
                query = "SELECT COUNT(*) FROM notes;"
                cursor.execute(query)
                result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
        except Exception as e:
            print(f"Error getting total notes count: {str(e)}")
            return 0  # Handle the error as needed, e.g., return an error response or raise a custom exception.
