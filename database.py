import sqlite3

def get_db():
    db = sqlite3.connect('system.db')
    db.row_factory = sqlite3.Row
    return db

def query_table(table_name):
    conn = get_db().cursor()
    conn.execute(f"SELECT * FROM {table_name}")
    data = conn.fetchall()
    return data

def insert_book(insert_details):
    conn = get_db()
    c = conn.cursor()
    sql_execute_string = f"INSERT INTO books (cover, title, author, description_book) VALUES (?, ?, ?, ?)"
    c.execute(sql_execute_string, insert_details)
    conn.commit()
    conn.close()

def delete_by_id(table_name, id):
    conn = get_db()
    conn.execute(f"DELETE FROM '{table_name}' WHERE id={id}")
    conn.commit()
    conn.close()

