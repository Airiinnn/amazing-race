import sqlite3

connection = sqlite3.connect("sqlite_db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM user")
users = cursor.fetchall()
connection.close()

print(users)