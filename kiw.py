from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'buku'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/')
def root():
    return 'Selamat datang di Toko Buku Sejahtera'

@app.route('/book', methods=['GET'])
def get_books():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    cursor.close()
    return jsonify(books)

@app.route('/book', methods=['POST'])
def add_book():
    data = request.get_json()
    name = data['name']
    deskripsi = data['deskripsi']
    harga = data['harga']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO book (name, deskripsi, harga) VALUES (%s, %s, %s)", (name, deskripsi, harga))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Book added successfully"})

@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    name = data['name']
    deskripsi = data['deskripsi']
    harga = data['harga']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE book SET name=%s, deskripsi=%s, harga=%s WHERE id=%s", (name, deskripsi, harga, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Book updated successfully"})

@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM book WHERE id=%s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
