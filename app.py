from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#init configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/api_contact'
db = SQLAlchemy(app)

#create models

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

#migrate apply
with app.app_context():
    db.create_all()

#Routes
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({'contacts': [contacts.serialize() for contacts in contacts]})

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(contact)
    db.session.commit()
    return jsonify({'contact': contact.serialize()}), 201

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return not_found()
    return jsonify({'contact': contact.serialize()})

@app.route('/contacts/<int:id>', methods=['PUT', 'PATCH'])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return not_found()
    data = request.get_json()
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']

    db.session.commit()
    return jsonify({'message': 'item updated successful', 'contact': contact.serialize()}), 200

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return not_found()
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'item delete successful'}), 200

def not_found():
    return jsonify({'message': 'not found'}), 404