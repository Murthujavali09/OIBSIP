import sqlite3
import re
import os

db_path = os.path.join(os.path.dirname(__file__), "database.db")
db = sqlite3.connect(db_path)
cursor = db.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    height REAL NOT NULL,
    weight REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

db.commit()


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def get_history(userid):
    cursor.execute(
        "SELECT date,height,weight,bmi,category FROM bmi_history WHERE user_id = ? ORDER BY date DESC", (userid,))
    rows = cursor.fetchall()
    return [
        {'date': row[0], 'height': row[1], 'weight': row[2],
            'bmi': row[3], 'category': row[4]}
        for row in rows
    ]


def insert_entry(userid, date, height, weight, bmi, category):
    cursor.execute(
        "INSERT INTO bmi_history (user_id,date,height,weight,bmi,category) VALUES (?,?,?,?,?,?) ",
        (userid, date, height, weight, round(bmi, 2), category)
    )
    db.commit()


def update_entry(userid, date, height, weight, bmi, category):
    cursor.execute(
        """UPDATE bmi_history SET height = ?, weight = ?,bmi = ?,category = ? 
           WHERE date = ? AND user_id = ?""",
        (height, weight, round(bmi, 2), category, date, userid)
    )
    db.commit()


def get_users_info(email, password):
    cursor.execute(
        "SELECT id FROM users WHERE email = ? AND password = ?", (email.lower(), password,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return -1


def email_exists(email):
    cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def create_user(name, email, password):
    cursor.execute(
        "INSERT INTO users (username,email,password) VALUES(?, ?, ?)", (name, email.lower(), password))
    db.commit()
    return cursor.lastrowid


def close():
    cursor.close()
    db.close()
