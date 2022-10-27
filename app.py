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


@app.cli.command('initdb') #decorator: on command line you can use initdb: lets you run your code from the command line, you can initalize data base without running the program
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

@app.route('/add', methods=['POST']) #url with /add will trigger the add fucntion, if the POST method is used
def add_entry():
    db = get_db() #looks into the database
    db.execute('insert into entries (title, category, text) values (?, ?, ?)', #SQL injection
               [request.form['title'], request.form['category'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

# Routes you to /delete, it is expecting to recieve a POST Command from show_entries.html
# No arguments are needed, and it will redirect you to the show_entries function on app.py where it will
# have the same webpage as before, but with one certain post deleted (depending on which entry's
# delete button (from the show_entries.html) was pressed)
@app.route('/delete', methods=['POST']) #url with /delete will trigger the delete fucntion, if the POST method is used
def delete_entry():
   db = get_db() #looks into the database
   db.execute("DELETE from entries WHERE id = ?", [request.form['item_id']])
   db.commit()
   flash('Entry Successfully Deleted')
   return redirect(url_for('show_entries'))

# Routes you to /edit, it is expecting to recieve a POST Command from edit_post.html
# No arguments are needed, and it will redirect you to the show_entries function on app.py where it will
# have the same webpage as before, but with one certain post edited (depending on which entry's
# edit button (from the show_entries.html) was pressed)
@app.route('/edit', methods=['POST'])
def edit_entry():
    db = get_db()
    db.execute('UPDATE entries SET title = ?, category = ?, text = ? WHERE id = ?',
               [request.form['title'], request.form['category'], request.form['text'], request.form['item_id']])
    db.commit()
    flash('Entry Successfully Updated')
    return redirect(url_for('show_entries'))

#Routes you to /edit_button, it is expecting to recieve a POST Command from show_entries.html.
# No arguments are needed, and it will take the item_id (from the selected post) and render the edit post form in
# edit_post.html. Through the item_id it will then prepopulate the form inputs with the current information (i.e. current
# titles, categories, text, and ids).
@app.route('/edit_button', methods=['POST'])
def edit_button():
    db = get_db()
    cur = db.execute('select title,category,text,id from entries WHERE id = ? order by id desc ', [request.form['item_id']])  # gets entries from the data base, cur pointer into the database
    entries = cur.fetchone()
    return render_template('edit_post.html', entries=entries)

