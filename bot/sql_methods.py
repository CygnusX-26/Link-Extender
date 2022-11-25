import sqlite3
from os.path import join, dirname, abspath

db_path = join(dirname(dirname(abspath(__file__))), 'FlaskApp/data/links.db')
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()
db_path2 = join(dirname(dirname(abspath(__file__))), 'FlaskApp/data/copypasta.db')
conn2 = sqlite3.connect(db_path2, check_same_thread=False)
c2 = conn2.cursor()


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


def getLinkCopy(name:str) -> list:
    c2.execute(
        f"SELECT * FROM copypasta WHERE extended = ?", (name,))
    return c2.fetchone()
    
def getAllCopy() -> list:
    c2.execute("SELECT * FROM copypasta")
    return c2.fetchall()

def insertLinkCopy(url:str, extended:str) -> None:
    with conn2:
        c2.execute(f"INSERT INTO copypasta VALUES (?, ?)", (url, extended))