import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (player1, player2, chance, winner) VALUES (?, ?, ?, ?)",
            ('Novak Djokovic', 'Roger Federer', 63, 'Novak Djokovic')
            )

connection.commit()
connection.close()