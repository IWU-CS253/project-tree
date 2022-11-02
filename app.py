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


@app.route('/', methods=['GET'])
def show_tree():
    db = get_db()
    cur = db.execute('SELECT name FROM characters')
    characters = cur.fetchall()
    return render_template('show_tree.html', characters=characters)


@app.route('/add-character', methods=['POST'])
def add_character():
    """Adds a new character"""
    db = get_db()
    name = request.form['name']
    db.execute('INSERT INTO characters (name) VALUES (?)',
               [name])
    db.commit()
    flash('Added ' + name)
    return redirect(url_for('show_tree'))

@app.route('/delete', methods=['POST'])
def delete_character():
    db = get_db()
    db.execute('delete from characters where id = ?', [request.form['id']])
    db.commit()
    flash('character was deleted')
    return redirect(url_for('show_tree'))

@app.route('/edit', methods=['POST'])
def edit_character():
    db = get_db()
    cur = db.execute('select name, id from characters where id = ?', [request.form['id']])
    characters = cur.fetchone()
    flash('moved to edit page')
    return render_template('edit.html', characters=characters)

@app.route('/save_edit', methods=['POST'])
def save_edit_character():
    db = get_db()
    db.execute('update characters set name = ? where id = ?', [request.form['name'], request.form['id']])
    db.commit()
    flash('character was edited')
    return redirect(url_for('show_tree'))