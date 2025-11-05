
from flask import Flask,render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///offers.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    offer_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Offer {self.title}>'

@app.route('/')
def home():
    
    return render_template('newHome.html')

@app.route('/info')
def info():
    return render_template('InfoPage.html')

@app.route('/creator_page')
def creator():
    return render_template('ListingCreation.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    full_path = os.path.abspath(db_path)
    print(f"Flask is reading from: {full_path}")
    print(f"File exists: {os.path.exists(full_path)}")
    if os.path.exists(full_path):
        print(f"File modified: {os.path.getmtime(full_path)}")
    
    offers = Offer.query.all()
    print(f"Flask sees {len(offers)} offers")
    for offer in offers:
        print(f"- {offer.title}: ${offer.price}")
    return render_template('services.html', offers=offers)

@app.route("/submit-offer", methods=['POST'])
def submit_offer():
    name = request.form['name']
    email = request.form['email']
    offer_type = request.form['offerType']
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    
    # Handle file upload (if image was uploaded)s
    image = request.files['image'] if 'image' in request.files else None
    image_filename = None
    
    if image and image.filename != '':
        # Save the image (you'll need to set up a folder for this)
        image_filename = secure_filename(image.filename)
        image.save(os.path.join('static/uploads', image_filename))
    
    # Insert into database
    conn = sqlite3.connect('instance/offers.db')  # Replace with your DB name
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO offer (name, email, offer_type, title, description, price, image_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, offer_type, title, description, price, image_filename))
    
    conn.commit()
    conn.close()
    
    # Redirect back to form or success page
    #flash('Offer submitted successfully!')
    return redirect(url_for('home'))
    pass

if __name__ == '__main__':
    with app.app_context():
        
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        full_path = os.path.abspath(db_path)
        print(f"Database file location: {full_path}")
        
        db.create_all()
        
        # Debug info - ADD THIS LINE
        existing_offers = Offer.query.all()
        print(f"Existing offers count: {len(existing_offers)}")
        
    
    print("Starting Flask app...")
    print("Visit: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)