from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nom_user = db.Column(db.String(80), nullable = False, unique = True)
    add_mail = db.Column(db.String(80), nullable = False, unique = True)
    mot_passe = db.Column(db.String(80), nullable = False)

    def __repr__(self):
        return f'<User {self.nom_user}>'
    
class Produits(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(80), nullable = False)
    prix = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(255), nullable = False)
    quantite = db.Column(db.Integer, nullable = False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    admin = db.relationship('Admin', backref=db.backref('produits', lazy=True))
    photo = db.Column(db.String)

    def __repr__(self):
        return f'<Produis {self.nom}>'
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.Integer, nullable = False, unique = True)
    add_mail = db.Column(db.String(80), nullable = False, unique = True)
    mot_passe = db.Column(db.String(255), nullable = False)
    photo = db.Column(db.String)

    def __repr__(self):
        return f'<Admin {self.user_name}>'
    
    