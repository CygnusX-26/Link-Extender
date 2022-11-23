from flask import Flask, redirect
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot.sql_methods import getLink, getAll
app = Flask(__name__)

@app.route('/<name>')
def index(name):
    return redirect(getLink(name)[0])


app.run()