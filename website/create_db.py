from database import get_db


def create_tables(db):
    conn = db.cursor()
    
    with open("tables.sql", 'r') as tables:
        conn.execute(tables.read())
        
    conn.close()
    return True


create_tables(get_db())
