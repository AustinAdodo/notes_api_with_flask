import sqlite3


class DB:
    path = "./workspace.db"

    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    @staticmethod
    def create_notes_table_if_not_exists():
        """In SQLite, you should use AUTOINCREMENT without the
             "AUTO" part. It should be AUTOINCREMENT or just INTEGER
              PRIMARY KEY for auto-incrementing primary keys"""
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL
        );
        """
        DB.cursor.execute(query)
        DB.conn.commit()

    @staticmethod
    def drop_notes_table_if_exists():
        DB.cursor.execute("DROP TABLE IF EXISTS notes;")
        DB.conn.commit()

    @staticmethod
    def create_note(content):
        query = "INSERT INTO notes (content) VALUES (?);"
        DB.cursor.execute(query, (content,))
        DB.conn.commit()
        return DB.cursor.lastrowid

    @staticmethod
    def update_note(note_id, content):
        query = "UPDATE notes SET content=? WHERE id=?;"
        DB.cursor.execute(query, (content, note_id))
        DB.conn.commit()
        return DB.cursor.rowcount

    @staticmethod
    def delete_note(note_id):
        query = "DELETE FROM notes WHERE id=?;"
        DB.cursor.execute(query, (note_id,))
        DB.conn.commit()
        return DB.cursor.rowcount

    @staticmethod
    def select_one_note(note_id):
        query = "SELECT * FROM notes WHERE id=?;"
        DB.cursor.execute(query, (note_id,))
        return DB.cursor.fetchone()

    @staticmethod
    def select_all_notes():
        DB.cursor.execute("SELECT * FROM notes;")
        return DB.cursor.fetchall()
