from flask import Flask, redirect, render_template, request, url_for
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot.sql_methods import getLink, getAll, insertLink, getLinkCopy, getAllCopy, insertLinkCopy
import validators
import lorem
import sqlite3
from os.path import join, dirname, abspath
import requests
import requests.auth
import json
import random
import urllib.parse
import secrets

USERID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET_KEY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
app = Flask(__name__)
db_path = join(dirname(dirname(abspath(__file__))), 'FlaskApp/data/links.db')
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()
db_path2 = join(dirname(dirname(abspath(__file__))), 'FlaskApp/data/copypasta.db')
conn2 = sqlite3.connect(db_path2, check_same_thread=False)
c2 = conn2.cursor()

DOMAIN = os.getenv("DOMAIN") + '/url/'
DOMAINPASTA = os.getenv("DOMAIN") + '/urlpasta/' 
random.seed()

def getAuth():
    #get token from reddit
    auth = requests.auth.HTTPBasicAuth(USERID, SECRET)
    data = {'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD}
    headers = {'User-Agent': 'LongerUrl/0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers

headers = getAuth()

def processInput(input: str) -> str:
    output = input
    output = output.replace(' ', '-')
    output = output.replace('.', '')
    output = output.replace(',', '')
    return output


@app.route('/url/<name>')
def url(name):
    link:str = getLink(name)[0]
    if (not(link.startswith("http://") or link.startswith("https://"))):
        link = "https://" + link
    return redirect(link)

@app.route('/urlpasta/<name>')
def urlPasta(name: str):
    link: str = getLinkCopy(urllib.parse.quote(name))[0] 
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
            if (not(url.startswith("http://") or url.startswith("https://"))):
                url = "https://" + url
            if not (validators.url(url) or validators.domain(url)):
                return render_template('index.html', show=True)
            all = getAll()
            extended = ""
            for _ in range(5):
                extended += lorem.paragraph()
            extended = extended.replace(' ', '-')
            extended = extended.replace('.', '')
            extended = extended.replace(',', '')
            for i in all:
                if (i[0] == url):
                    return render_template('index.html', show=False, inputurl=url, extended=DOMAIN + i[1])
                if (i[1] == extended):
                    extended = extended + secrets.token_hex(1)
            insertLink(url, extended)
            return render_template('index.html', show=False, inputurl=url, extended=DOMAIN + extended)
        if (filler == 'copypasta'):
            if (not(url.startswith("http://") or url.startswith("https://"))):
                url = "https://" + url
            if not (validators.url(url) or validators.domain(url)):
                return render_template('index.html', show=True)
            all = getAllCopy()
            try:
                res = requests.get("https://oauth.reddit.com/r/copypasta/random", headers=headers)
                extended = res.json()[0]['data']['children'][0]['data']['title'] + ": " + res.json()[0]['data']['children'][0]['data']['selftext']  # let's see what we get
            except:
                headers = getAuth()
                res = requests.get("https://oauth.reddit.com/r/copypasta/random", headers=headers)
                extended = res.json()[0]['data']['children'][0]['data']['title'] + ": " + res.json()[0]['data']['children'][0]['data']['selftext']  # actually get the request now
            for i in all:
                if (i[0] == url):
                    return render_template('index.html', show=False, inputurl=url, extended=DOMAINPASTA + i[1])
                if (i[1] == extended):
                    extended = extended + secrets.token_hex(1)
            extended = processInput(extended)
            processed = urllib.parse.quote(extended)
            insertLinkCopy(url, processed)
            return render_template('index.html', show=False, inputurl=url, extended=DOMAINPASTA + urllib.parse.unquote(processed),)
    else:
        return render_template('index.html', show=True)

try:
    c.execute("""CREATE TABLE links (
            url text,
            extended text
            )""")
except:
    pass

try:
    c2.execute("""CREATE TABLE copypasta (
            url text,
            extended text
            )""")
except:
    pass
res = requests.get("https://oauth.reddit.com/r/copypasta/random", headers=headers)

#tester text
"""
extended = "😂"
print(urllib.parse.quote(extended))


if len(extended) > 1800:  #arbitrary length chosen to suite most web browsers
    offset = random.randint(0,len(extended) - 1800)
    extended = extended[0 + offset:1800 + offset]
size = 16
chunks = [extended[x:x+size] for x in range(0, len(extended), size)]#size chosen to be less than 64, the limit for idna
processed = []
for chunk in chunks:
    print(chunk)
    processed.append(chunk.encode(encoding="idna"))
processed = b''.join(processed)
print("final results")
print(processed)
print("back to uni")
print(processed.decode("idna"))"""


app.run()