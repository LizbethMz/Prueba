import sqlite3

conn = sqlite3.connect('liz.db')
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS clientes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   telefono TEXT
               )
""")

cursor.execute("""
               INSERT INTO clientes (nombre, telefono) 
               VALUES('Juan Perez', '123456')
""")

conn.commit()


conn.close()