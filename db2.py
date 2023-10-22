import sqlite3


# fetch all the data
# print(cursor.fetchall())
class DB2:
    # path = "./workspace.db"
    path = "./notes.db"

    conn = sqlite3.connect(path, check_same_thread=False)  # con = sqlite3.connect("workspace.db")
    conn.row_factory = sqlite3.Row
    # create the cursor object
    cursor = conn.cursor()

    @staticmethod
    def create_notes_table_if_not_exists():
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        );
        """
        # DB2.cursor.execute(query)
        DB2.cursor.executescript(query)
        DB2.conn.commit()

    @staticmethod
    def drop_notes_table_if_exists():
        DB2.cursor.execute("DROP TABLE IF EXISTS notes;")
        DB2.conn.commit()

    @staticmethod
    def create_note(val):
        cur = DB2.cursor
        query = "INSERT INTO notes (content) VALUES (?);"
        DB2.cursor.execute(query, (val,))
        DB2.conn.commit()
        return DB2.cursor.lastrowid

    @staticmethod
    def update_note(note_id, content):
        query = "UPDATE notes SET content=? WHERE id=?;"
        DB2.cursor.execute(query, (content, note_id))
        DB2.conn.commit()
        return DB2.cursor.rowcount

    @staticmethod
    def delete_note(note_id):
        query = "DELETE FROM notes WHERE id=?;"
        DB2.cursor.execute(query, (note_id,))
        DB2.conn.commit()
        return DB2.cursor.rowcount

    @staticmethod
    def select_one_note(note_id):
        query = "SELECT * FROM notes WHERE id=?;"
        DB2.cursor.execute(query, (note_id,))
        result = DB2.cursor.fetchone()
        return result

    @staticmethod
    def select_all_notes():
        DB2.cursor.execute("SELECT * FROM notes;")
        return DB2.cursor.fetchall()
