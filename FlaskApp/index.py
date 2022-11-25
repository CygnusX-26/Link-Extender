from flask import Flask, redirect, render_template, request, url_for
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot.sql_methods import getLink, getAll, insertLink
import validators
import lorem
import sqlite3
from os.path import join, dirname, abspath
import requests

app = Flask(__name__)
db_path = join(dirname(dirname(abspath(__file__))), 'FlaskApp/data/links.db')
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()
DOMAIN = 'http://127.0.0.1:5000/url/'

@app.route('/url/<name>')
def url(name):
    link = getLink(name)[0]
    if (not(link.startswith("http://") or link.startswith("https://"))):
        link = "https://" + link
    return redirect(link)


@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST' and request.form.get('inputurl') and request.form.get('fillertype')):
        url = request.form.get('inputurl')
        filler = request.form.get('fillertype')
        print(url, filler)
        if (filler == 'latin'):
            if not (validators.url(url) or validators.domain(url)):
                return render_template('index.html', show=True)
            all = getAll()
            for i in all:
                if (i[0] == url):
                    return render_template('index.html', show=False, extended=DOMAIN + i[1])
            extended = ""
            for _ in range(5):
                extended += lorem.paragraph()
            extended = extended.replace(' ', '-')
            extended = extended.replace('.', '')
            extended = extended.replace(',', '')
            insertLink(url, extended)
            return render_template('index.html', show=False, url=url, extended=DOMAIN + extended)
    return render_template('index.html', show=True)

try:
    c.execute("""CREATE TABLE links (
            url text,
            extended text
            )""")
except:
    pass

app.run()