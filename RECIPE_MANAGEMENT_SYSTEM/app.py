from flask import Flask, render_template, request, redirect, url_for, flash, session, g, send_file
import sqlite3
import os
import hashlib
import io

app = Flask(__name__)
app.secret_key = 'shreyashguptakey'

DATABASE = 'recipes.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        category_id INTEGER,
        name TEXT,
        ingredients TEXT,
        instructions TEXT,
        dish_image BLOB,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    CHECK(length(comment_text) <= 500)
)''')

    users = [
        ('admin', hashlib.sha256('admin'.encode()).hexdigest()),
        ('shreyash', hashlib.sha256('shreyashguptacdac'.encode()).hexdigest()),
        ('shivam', hashlib.sha256('shivam'.encode()).hexdigest())
    ]
    for username, password_hash in users:
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        if c.fetchone() is None:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))

    conn.commit()
    conn.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user:
            hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_input_password == user['password']:
                session['logged_in'] = True
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
        flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/index')
def index():
    if 'logged_in' not in session:
        flash('You must be logged in to access the main page.', 'warning')
        return redirect(url_for('login'))

    db = get_db()
    categories = db.execute('SELECT * FROM categories').fetchall()
    return render_template('index.html', categories=categories)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/category/<int:category_id>')
def category(category_id):
    db = get_db()
    recipes = db.execute('SELECT id, name FROM recipes WHERE category_id=?', (category_id,)).fetchall()
    category = db.execute('SELECT name FROM categories WHERE id=?', (category_id,)).fetchone()
    return render_template('category.html', recipes=recipes, category=category)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    db = get_db()
    recipe = db.execute('SELECT * FROM recipes WHERE id=?', (recipe_id,)).fetchone()
    comments = db.execute('SELECT * FROM comments WHERE recipe_id=? ORDER BY created_at DESC', (recipe_id,)).fetchall()
    return render_template('recipe.html', recipe=recipe, comments=comments)



@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    if 'logged_in' not in session:
        flash('Login required to add a recipe.', 'warning')
        return redirect(url_for('login'))

    category_id = request.form['category_id']
    name = request.form['name']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']
    image_file = request.files['image']
    image_data = image_file.read()

    db = get_db()
    db.execute(''' 
        INSERT INTO recipes (category_id, name, ingredients, instructions, dish_image)
        VALUES (?, ?, ?, ?, ?)
    ''', (category_id, name, ingredients, instructions, image_data))
    db.commit()

    flash('Recipe added!', 'success')
    return redirect(url_for('category', category_id=category_id))

@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    if 'logged_in' not in session:
        flash('You must be logged in to delete a recipe.', 'warning')
        return redirect(url_for('login'))

    recipe_name = request.form.get('delete_name', '').strip()
    if not recipe_name:
        flash('Please enter a recipe name to delete.', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    recipe = db.execute('SELECT id, category_id FROM recipes WHERE name = ?', (recipe_name,)).fetchone()

    if recipe:
        db.execute('DELETE FROM recipes WHERE id = ?', (recipe['id'],))
        db.commit()
        flash(f'Recipe "{recipe_name}" has been deleted.', 'success')
        return redirect(url_for('category', category_id=recipe['category_id']))
    else:
        flash(f'No recipe found with the name "{recipe_name}".', 'danger')
        return redirect(url_for('index'))


@app.route('/add_comment/<int:recipe_id>', methods=['POST'])
def add_comment(recipe_id):
    if 'logged_in' not in session:
        flash('You must be logged in to comment.', 'warning')
        return redirect(url_for('login'))

    comment_text = request.form['comment']
    user_name = session['username']  

    db = get_db()
    db.execute('''
        INSERT INTO comments (recipe_id, user_name, comment_text)
        VALUES (?, ?, ?)
    ''', (recipe_id, user_name, comment_text))
    db.commit()

    flash('Your comment has been posted.', 'success')
    return redirect(url_for('recipe', recipe_id=recipe_id))



@app.route('/recipe_image/<int:recipe_id>')
def recipe_image(recipe_id):
    db = get_db()
    cur = db.execute('SELECT dish_image FROM recipes WHERE id=?', (recipe_id,))
    row = cur.fetchone()
    if row and row['dish_image']:
        try:
            return send_file(io.BytesIO(row['dish_image']), mimetype='image/jpeg')
        except Exception as e:
            print("Error serving image:", e)
            return send_file('static/no_image.jpg', mimetype='image/jpeg')
    else:
        return send_file('static/no_image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
