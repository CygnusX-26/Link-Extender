import sqlite3
from os.path import join, dirname, abspath

db_path = join(dirname(dirname(abspath(__file__))), 'bot/data/links.db')
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()


def getLink(name:str) -> list:
    c.execute(
        f"SELECT * FROM links WHERE extended = ?", (name,))
    return c.fetchone()
    
def getAll() -> list:
    c.execute("SELECT * FROM links")
    return c.fetchall()

def insertLink(url:str, extended:str) -> None:
    with conn:
        c.execute(f"INSERT INTO links VALUES (?, ?)", (url, extended))