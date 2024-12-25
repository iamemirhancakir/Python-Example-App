import sqlite3

class DatabaseManager:
    def __init__(self, db_name="finance_app.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Gelir tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        ''')
        # Gider tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()

    def add_income(self, amount, category, date):
        """Gelir ekler."""
        self.cursor.execute("INSERT INTO income (amount, category, date) VALUES (?, ?, ?)", (amount, category, date))
        self.conn.commit()

    def add_expense(self, amount, category, date):
        """Gider ekler."""
        self.cursor.execute("INSERT INTO expense (amount, category, date) VALUES (?, ?, ?)", (amount, category, date))
        self.conn.commit()

    def get_all_income(self):
        """Tüm gelirleri getirir."""
        self.cursor.execute("SELECT * FROM income")
        return self.cursor.fetchall()

    def get_all_expenses(self):
        """Tüm giderleri getirir."""
        self.cursor.execute("SELECT * FROM expense")
        return self.cursor.fetchall()

    def get_total_income(self):
        self.cursor.execute("SELECT SUM(amount) FROM income")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0.0

    def get_total_expenses(self):
        self.cursor.execute("SELECT SUM(amount) FROM expense")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0.0

    def close(self):
        """Veritabanı bağlantısını kapatır."""
        self.conn.close()

    def get_filtered_income(self, date=None, category=None):
        query = "SELECT * FROM income WHERE 1=1"
        params = []

        if date:
            query += " AND date = ?"
            params.append(date)

        if category:
            query += " AND category = ?"
            params.append(category)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_filtered_expenses(self, date=None, category=None):
        query = "SELECT * FROM expense WHERE 1=1"
        params = []

        if date:
            query += " AND date = ?"
            params.append(date)

        if category:
            query += " AND category = ?"
            params.append(category)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()
