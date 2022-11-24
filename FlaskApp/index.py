from flask import Flask, redirect, render_template, request, url_for
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot.sql_methods import getLink, getAll, insertLink
import validators
import lorem
import sqlite3
from os.path import join, dirname, abspath

app = Flask(__name__)
db_path = join(dirname(dirname(abspath(__file__))), 'bot/data/links.db')
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()
DOMAIN = 'http://127.0.0.1:5000/'

@app.route('/<name>')
def url(name):
    link = getLink(name)[0]
    if (not(link.startswith("http://") or link.startswith("https://"))):
        link = "https://" + link
    return redirect(link)

@app.route('/', methods=['GET'])
def index():
    if (request.method == 'GET' and request.args.get('inputurl') and request.args.get('fillertype')):
        url = request.args.get('inputurl')
        filler = request.args.get('fillertype')
        if (filler == 'latin'):
            if not (validators.url(url) or validators.domain(url)):
                return render_template('index.html', show=True)
            extended = ""
            for _ in range(5):
                extended += lorem.paragraph()
            extended = extended.replace(' ', '-')
            extended = extended.replace('.', '')
            extended = extended.replace(',', '')
            insertLink(url, extended)
            return render_template('index.html', show=False, url=url, extended=(f"{DOMAIN}" + extended))
    return render_template('index.html', show=True)

try:
    c.execute("""CREATE TABLE links (
            url text,
            extended text
            )""")
except:
    pass

app.run()