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
import random
import string

from werkzeug.security import generate_password_hash, check_password_hash

import create_implicits
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash, session

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
    tree_id = request.args['tree_id']
    cur = db.execute('SELECT tree_name, tree_id FROM trees WHERE tree_id = ?', [tree_id])
    tree = cur.fetchone()

    cur = db.execute('SELECT color, type, tree_id_color FROM colors WHERE tree_id_color = ?', [tree_id])
    colors = cur.fetchall()

    # checks if the colors table is empty for that tree if it is add default values
    if len(colors) == 0:
        db.execute('INSERT INTO colors (tree_id_color, color, type) VALUES (?, ?, ?)',
                   [tree_id, "#0000ff", "Parent - Child"])
        db.commit()
        db.execute('INSERT INTO colors (tree_id_color, color, type) VALUES (?, ?, ?)',
                   [tree_id, "#00ff00", "Sibling - Sibling"])
        db.commit()
        db.execute('INSERT INTO colors (tree_id_color, color, type) VALUES (?, ?, ?)',
                   [tree_id, "#ff0000", "Spouse - Spouse"])
        db.commit()
        db.execute('INSERT INTO colors (tree_id_color, color, type) VALUES (?, ?, ?)',
                   [tree_id, "#ffa500", "Partner - Partner"])
        db.commit()

    cur = db.execute('SELECT name, id, tree_id_character FROM characters WHERE tree_id_character = ?', [tree_id])
    characters = cur.fetchall()

    cur = db.execute('SELECT DISTINCT r.character1, r.character2, r.type, r.description, c1.name AS "char1_name", c2.name AS "char2_name", clr.color AS "color" '
                     'FROM relationships AS r JOIN characters AS c1 ON r.character1 = c1.id '
                     'JOIN characters AS c2 ON r.character2 = c2.id '
                     'JOIN colors AS clr ON r.type = clr.type WHERE r.tree_id_relationship = ? AND tree_id_color = ?', [tree_id, tree_id])

    relationships = cur.fetchall()
    for relationship in relationships:
        print(relationship['CHARACTER1'])
    implicit_rels = create_implicits.merge_implicits(characters, relationships)

    generations = create_implicits.create_generations(characters, relationships)

    generations = update_generation(generations)

    generation_list = unique_generation(generations)
    
    return render_template('show_tree.html', tree=tree, characters=characters, relationships=relationships, colors=colors, implicits=implicit_rels, generations=generations, generation_list=generation_list)


@app.route('/', methods=['GET'])
def home_page():
    string_letters = string.ascii_lowercase
    if 'guest_code' not in session:
        guest_word = ''
        for i in range(25):
            guest_word = guest_word + string_letters[random.randint(0, 25)]
        session['guest_code'] = guest_word

    user = find_user()


    db = get_db()
    cur = db.execute('SELECT tree_name, tree_id FROM trees WHERE username = \'{}\''.format(user))
    trees = cur.fetchall()
    return render_template('homepage.html', trees=trees, user=user)


@app.route('/add-tree', methods=['POST'])
def add_tree():
    """Adds a Tree"""


    user = find_user()

    db = get_db()
    tree_name = request.form['tree_name']
    cur = db.execute('SELECT tree_name FROM trees  WHERE EXISTS(SELECT tree_name, username FROM trees WHERE tree_name = ? AND username = ? ) ',
               [tree_name, user])
    tree = cur.fetchone()
    if tree:
        flash('Please add a unique tree name')
        return redirect(url_for('home_page'))
    db.execute('INSERT INTO trees (tree_name, username) VALUES (?, ?)',
               [tree_name, user])
    db.commit()

    flash('Added ' + tree_name)
    return redirect(url_for('home_page'))


@app.route('/add-character', methods=['POST'])
def add_character():
    """Adds a new character"""
    db = get_db()
    name = request.form['name']
    tree_id = request.form['tree_id']
    character_generation = request.form['character_generation']
    db.execute('INSERT INTO characters (name, tree_id_character, generation) VALUES (?, ?, ?)',
               [name, tree_id, character_generation])
    db.commit()
    flash('Added ' + name)
    return redirect(url_for('show_tree', tree_id=tree_id))


@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    db = get_db()
    tree_id = request.form['tree_id']

    rel_type = request.form['type']
    char1 = request.form['character1']
    char2 = request.form['character2']
    if char1 == char2:
        flash('Character cannot be in a relationship with themselves')
        return redirect(url_for('show_tree', tree_id=tree_id))

    if rel_type == 'Parent - Child':
        cur = db.execute('SELECT name, id, tree_id_character FROM characters WHERE tree_id_character = ?', [tree_id])
        characters = cur.fetchall()

        cur = db.execute(
            'SELECT r.character1, r.character2, r.type, r.description, c1.name AS "char1_name", c2.name AS "char2_name" '
            'FROM relationships AS r JOIN characters AS c1 ON r.character1 = c1.id '
            'JOIN characters AS c2 ON r.character2 = c2.id WHERE r.tree_id_relationship = ?', [tree_id])
        relationships = cur.fetchall()

        if create_implicits.check_loops(characters, relationships, char1, char2):
            flash('Character cannot be their own ancestor')
            return redirect(url_for('show_tree', tree_id=tree_id))

    if rel_type == 'Custom':
        rel_type = request.form['custom_type']
        db.execute('INSERT INTO colors (tree_id_color, color, type) VALUES (?,?,?)',
            [tree_id, "#FF0000", rel_type])
        db.commit()

    db.execute('INSERT INTO relationships (character1, character2, type, description, tree_id_relationship) VALUES (?,?,?,?,?)',
                [char1, char2, rel_type, request.form['description'], tree_id])
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
    cur = db.execute('select id, name from characters where id = ? and tree_id_character = ?',
                     [request.form['id'], tree_id])
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


@app.route('/register', methods=['POST'])
def register():
    db = get_db()
    username = request.form['username']
    cur = db.execute('SELECT username FROM accounts  WHERE EXISTS (SELECT username FROM accounts WHERE username = ?) ',
               [request.form['username']])
    name = cur.fetchone()
    if name:
        flash('Username Taken, Please select a different username')
        return redirect(url_for('show_register'))
    password = generate_password_hash(request.form['password'], "sha256")
    db.execute('INSERT INTO accounts (username, password_hash) VALUES (?,?)',
               [username, password])
    db.commit()
    flash('Account Created')
    return redirect(url_for('home_page'))


@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    cur = db.execute('SELECT username FROM accounts  WHERE EXISTS (SELECT username FROM accounts WHERE username = ?) ',
               [request.form['username']])
    name = cur.fetchone()
    if not name:
        flash('Incorrect username or password')
        return redirect(url_for('show_login'))
    cur = db.execute('SELECT password_hash FROM accounts WHERE username = ?',
                     [request.form['username']])
    database = cur.fetchone()

    if check_password_hash(database[0], request.form['password']):
        session['username'] = request.form['username']

        flash('You were logged in')
        return redirect(url_for('home_page'))
    else:
        flash('Incorrect username or password')
        return redirect(url_for('show_login'))

    return render_template('homepage')


@app.route('/logout')
def logout():
    session.pop('username', None)

    flash('You were logged out')
    return redirect(url_for('home_page'))


@app.route('/show_register', methods=['GET'])
def show_register():
    return render_template('show_register.html')


@app.route('/show_login', methods=['GET'])
def show_login():
    return render_template('show_login.html')


@app.route('/delete_tree', methods=['POST'])
def delete_tree():
    db = get_db()
    tree_id = request.form['tree_id']
    db.execute('DELETE FROM trees WHERE tree_id = ?',
               [tree_id])
    db.commit()
    flash('tree was deleted')
    return redirect(url_for('home_page'))

@app.route('/add_color', methods=['POST'])
def add_color():
    db = get_db()
    relationship_type = request.form['type']
    color = request.form['color']
    tree_id = request.form['tree_id']
    db.execute('UPDATE colors SET color = ? WHERE type = ? AND tree_id_color = ?',
               [color, relationship_type, tree_id])
    db.commit()
    return redirect(url_for('show_tree', tree_id=tree_id))


# For run configurations to test the create_implicits graphs
@app.cli.command('testgraph')
def implicit_test_graph():
    create_implicits.test_graph()


def find_user():
    if 'username' in session:
        user = session['username']

    else:
        user = session['guest_code']

    return user


@app.route('/edit_generation', methods=['POST'])
def edit_generation():
    generation = request.form['generation']
    tree_id = request.form['tree_id']
    db = get_db()
    db.execute('UPDATE characters SET generation = ? WHERE id = ?', [generation, request.form['id']])
    db.commit()
    flash('Character Generation Updated')
    return redirect(url_for('show_tree', tree_id=tree_id))


def update_generation(graph):
    db = get_db()
    cur =  db.execute('SELECT generation, id FROM characters')
    generations = cur.fetchall()
    for i in range(len(generations)):
        if generations[i][0] != 50:
            updated_pair = {generations[i][1]: generations[i][0]}
            graph.update(updated_pair)
    return graph


def unique_generation(graph):
    new_list = graph.keys()
    generation_tracker = []
    for i in new_list:
        if not graph[i] in generation_tracker:
            new_num = graph[i]
            generation_tracker.append(new_num)
    return generation_tracker
