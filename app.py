# -*- coding: utf-8 -*-
"""
    Family Tree Creator
    ---------------------

    Some Code was Adapted from:
    Flaskr by Armin Ronacher.

    A simple webapp for creating family trees for fictional characters
    and real families alike. Built on code from the Flaskr Microblogger Webapp.
    See LICENSE for more details.
"""


import os
import create_implicits
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
    cur = db.execute('SELECT tree_name, tree_id FROM trees WHERE tree_id = ?', [request.args['tree_id']])
    tree = cur.fetchone()

    cur = db.execute('SELECT name, id, tree_id_character FROM characters WHERE tree_id_character = ?', [request.args['tree_id']])
    characters = cur.fetchall()

    cur = db.execute('SELECT r.character1, r.character2, r.type, r.description, c1.name AS "char1_name", c2.name AS "char2_name" '
                     'FROM relationships AS r JOIN characters AS c1 ON r.character1 = c1.id '
                     'JOIN characters AS c2 ON r.character2 = c2.id WHERE r.tree_id_relationship = ?', [request.args['tree_id']])
    relationships = cur.fetchall()

    relationships = create_implicits.merge_implicits(characters, relationships)[0]

    hierarchy = create_implicits.create_hierarchy(characters, relationships)
   # hierarchy = create_implicits.update_hierarchy(characters, relationships, hierarchy)

    return render_template('show_tree.html', tree=tree, characters=characters, relationships=relationships, hierarchy=hierarchy)

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

@app.route('/add-character', methods=['POST'])
def add_character():
    """Adds a new character"""
    db = get_db()
    name = request.form['name']
    tree_id = request.form['tree_id']
    db.execute('INSERT INTO characters (name, tree_id_character) VALUES (?, ?)',
               [name, tree_id])
    db.commit()
    flash('Added ' + name)
    return redirect(url_for('show_tree', tree_id=tree_id))


@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    db = get_db()
    tree_id = request.form['tree_id']
    var = request.form['type']
    if var == 'Custom':
        var == request.form['custom_type']
    db.execute('INSERT INTO relationships (character1, character2, type, description, tree_id_relationship) VALUES (?,?,?,?,?)',
                [request.form['character1'], request.form['character2'], request.form['type'], request.form['description'], tree_id])
    db.commit()
    flash('added relationship')
    return redirect(url_for('show_tree', tree_id=tree_id))


@app.route('/delete', methods=['POST'])
def delete_character():
    db = get_db()
    tree_id = request.form['tree_id']
    db.execute('delete from characters where id = ?', [request.form['id']])
    db.commit()
    flash('character was deleted')
    return redirect(url_for('show_tree', tree_id=tree_id))


@app.route('/edit', methods=['POST'])
def edit_character():
    db = get_db()
    tree_id = request.form['tree_id']
    cur = db.execute('select id, name from characters where id = ? and tree_id_character = ?', [request.form['id'], tree_id])
    characters = cur.fetchone()
    return render_template('edit.html', characters=characters, tree_id=tree_id)


@app.route('/save_edit', methods=['POST'])
def save_edit_character():
    db = get_db()
    tree_id = request.form['tree_id']
    db.execute('update characters set name = ? where id = ?', [request.form['name'], request.form['id']])
    db.commit()
    flash('character was edited')
    return redirect(url_for('show_tree', tree_id=tree_id))


@app.route('/delete_relationship', methods=['POST'])
def delete_relationship():
    db = get_db()
    tree_id = request.form['tree_id']
    db.execute('DELETE FROM relationships WHERE character1 = ? AND character2 = ?',
               [request.form['character1'], request.form['character2']])
    db.commit()
    flash('relationship was deleted')
    return redirect(url_for('show_tree', tree_id=tree_id))


# For run configurations to test the create_implicits graphs
@app.cli.command('testgraph')
def implicit_test_graph():
    create_implicits.test_graph()
