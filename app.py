from flask import Flask, render_template, redirect, url_for, flash, request
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi koneksi database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        database='flask_crud',
        password=''
    )

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/items')
def item_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('item_list.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (name, description))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Item created successfully!', 'success')
        return redirect(url_for('item_list'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
    item = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cursor.execute('UPDATE items SET name = %s, description = %s WHERE id = %s', (name, description, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('item_list'))

    cursor.close()
    conn.close()
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('item_list'))

if __name__ == '__main__':
    app.run(debug=True)