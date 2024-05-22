import sqlite3
class Auth:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                password TEXT
                            )''')
        self.conn.commit()
    
    def get_registered_users(self):
        self.cursor.execute("SELECT username FROM users")
        return self.cursor.fetchall()

    def register(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True, " ✅ Registration successful."
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            return True, " ✅ Login successful."
        else:
            return False, " Invalid username or password."




    def close_connection(self):
        self.conn.close()
