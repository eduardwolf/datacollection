import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'database.db'

#  connect to DB
def get_db():
    db = getattr(Flask, '_database', None)
    if db is None:
        db = Flask._database = sqlite3.connect(DATABASE, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db


# Read all - GET http://localhost:5000/listings
@app.route('/listings', methods=['GET'])
def get_listings():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM listings')
    listings = cur.fetchall()
    return jsonify([dict(listing) for listing in listings])


# Read by ID - GET http://localhost:5000/listings/"listing_id"
@app.route('/listings/<string:listing_id>', methods=['GET'])
def get_listing(listing_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM listings WHERE listing_id = ?', (listing_id,))
    listing = cur.fetchone()
    if listing is None:
        return jsonify({'error': 'Listing not found'}), 404
    return jsonify(dict(listing))


# Create - POST http://localhost:5000/listings
@app.route('/listings', methods=['POST'])
def create_listing():
    db = get_db()
    cur = db.cursor()
    listing = request.json
    cur.execute('INSERT INTO listings (listing_id, status, term, rooms, interior, exterior, price, floor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (listing['listing_id'], listing['status'], listing['term'], listing['rooms'], listing['interior'], listing['exterior'], listing['price'], listing['floor']))
    db.commit()
    return jsonify({'message': 'Listing created successfully'})


# Update - PUT http://localhost:5000/listings/"listing_id"
@app.route('/listings/<string:listing_id>', methods=['PUT'])
def update_listing(listing_id):
    db = get_db()
    cur = db.cursor()
    listing = request.json
    cur.execute('UPDATE listings SET status = ?, term = ?, rooms = ?, interior = ?, exterior = ?, price = ?, floor = ? WHERE listing_id = ?',
                (listing['status'], listing['term'], listing['rooms'], listing['interior'], listing['exterior'], listing['price'], listing['floor'], listing_id))
    db.commit()
    return jsonify({'message': 'Listing updated successfully'})


# Delete - DELETE http://localhost:5000/listings/"listing_id"
@app.route('/listings/<string:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM listings WHERE listing_id = ?', (listing_id,))
    db.commit()
    return jsonify({'message': 'Listing deleted successfully'})


if __name__ == '__main__':
    app.run()
