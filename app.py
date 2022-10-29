# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'tree.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET']) #specifing in the url what resource you want to access. Backend takes request and figures out what resource this is for.
def show_entries():
    db = get_db()
    cur = db.execute('select title,category,text,id from entries order by id desc') #gets entries from the data base, cur pointer into the database
    entries = cur.fetchall() #actually retrieves data from cur (returns list of selected data)
    cur_filter = db.execute('SELECT DISTINCT category from entries order by id desc')
    distinct_cats = cur_filter.fetchall()
    #cat_filter = request.args.get('filter_cats')
    if "category" in request.args:
        cur = db.execute("SELECT title,text,category,id from entries WHERE category = ? ORDER BY id desc", [request.args["category"]])
        entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries, distinct_cats=distinct_cats) #puts the list into a template