# -*- coding: utf-8 -*-
"""
    Family Tree Creator
    ---------------------

    Some Code was Adapted from:
    Flaskr

    A simple webapp for creating family trees for fictional characters
    and real families alike. Built on code from the Flaskr Microblogger Webapp.
    See LICENSE for more details.

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
    g.sqlite_db.execute('pragma foreign_keys=on')
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/tree', methods=['GET'])
def show_tree():
    db = get_db()
    cur = db.execute('SELECT name FROM characters')
    characters = cur.fetchall()
    cur = db.execute('SELECT character1, character2, type, description FROM relationships')
    relationships = cur.fetchall()
    return render_template('show_tree.html', characters=characters, relationships=relationships)

@app.route('/', methods=['GET'])
def home_page():
    db = get_db()
    cur = db.execute('SELECT tree_name, tree_id FROM trees')
    trees = cur.fetchall()
    return render_template('homepage.html', trees=trees)

@app.route('/add-tree', methods=['POST'])
def add_tree():
    """Adds a new tree"""
    db = get_db()
    tree_name = request.form['tree_name']
    db.execute('INSERT INTO trees (tree_name) VALUES (?)',
               [tree_name])
    db.commit()
    flash('Added ' + tree_name)
    return redirect(url_for('home_page'))

@app.route('/home_trees', methods=['POST'])
def home_trees():
    db = get_db()
    cur = db.execute('select tree_name id from trees')
    trees = cur.fetchall()
    flash('page is showing trees')
    return render_template('homepage.html', trees=trees)

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


@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    db = get_db()
    if request.form['type'] == 'Custom':
        db.execute('INSERT INTO relationships (character1, character2, type, description) VALUES (?,?,?,?)',
                   [request.form['character1'], request.form['character2'], request.form['custom_type'], request.form['description']])
    else:
        db.execute('INSERT INTO relationships (character1, character2, type, description) VALUES (?,?,?,?)',
                   [request.form['character1'], request.form['character2'], request.form['type'], request.form['description']])
    db.commit()
    flash('added relationship')
    return redirect(url_for('show_tree'))


@app.route('/delete', methods=['POST'])
def delete_character():
    db = get_db()
    db.execute('delete from characters where name = ?', [request.form['name']])
    db.commit()
    flash('character was deleted')
    return redirect(url_for('show_tree'))


@app.route('/edit', methods=['POST'])
def edit_character():
    db = get_db()
    cur = db.execute('select name from characters where name = ?', [request.form['name']])
    characters = cur.fetchone()
    flash('moved to edit page')
    return render_template('edit.html', characters=characters)


@app.route('/save_edit', methods=['POST'])
def save_edit_character():
    db = get_db()
    db.execute('update characters set name = ? where name = ?', [request.form['name'], request.form['rename']])
    db.commit()
    flash('character was edited')
    return redirect(url_for('show_tree'))
