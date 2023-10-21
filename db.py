


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
        cls.cursor.execute(query)
        cls.conn.commit()

    @classmethod
    def drop_notes_table_if_exists(cls):
        cls.cursor.execute("DROP TABLE IF EXISTS notes;")
        cls.conn.commit()

    @classmethod
    def create_note(cls, content):
        query = "INSERT INTO notes (content) VALUES (?);"
        cls.cursor.execute(query, (content,))
        cls.conn.commit()
        return cls.cursor.lastrowid

    @classmethod
    def update_note(cls, note_id, content):
        query = "UPDATE notes SET content=? WHERE id=?;"
        cls.cursor.execute(query, (content, note_id))
        cls.conn.commit()
        return cls.cursor.rowcount

    @classmethod
    def delete_note(cls, note_id):
        query = "DELETE FROM notes WHERE id=?;"
        cls.cursor.execute(query, (note_id,))
        cls.conn.commit()
        return cls.cursor.rowcount

    @classmethod
    def select_one_note(cls, note_id):
        query = "SELECT * FROM notes WHERE id=?;"
        cls.cursor.execute(query, (note_id,))
        return cls.cursor.fetchone()

    @classmethod
    def select_all_notes(cls):
        cls.cursor.execute("SELECT * FROM notes;")
        return cls.cursor.fetchall()
