from flask import Flask, redirect, render_template, request, url_for
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot.sql_methods import getLink, getAll, insertLink
import validators
import lorem

app = Flask(__name__)

@app.route('/<name>')
def url(name):
    return redirect(getLink(name)[0])

@app.route('/', methods=['GET'])
def index():
    if (request.method == 'GET' and request.args.get('inputurl') and request.args.get('fillertype')):
        url = request.args.get('inputurl')
        filler = request.args.get('fillertype')
        if (filler == 'latin'):
            if not validators.url(url):
                return render_template('index.html', show=True)
            extended = ""
            for _ in range(5):
                extended += lorem.paragraph()
            extended = extended.replace(' ', '-')
            extended = extended.replace('.', '')
            extended = extended.replace(',', '')
            insertLink(url, extended)
            return render_template('index.html', show=False, url=url, extended=("http://127.0.0.1:5000/" + extended))
    return render_template('index.html', show=True)


app.run()