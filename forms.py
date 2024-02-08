from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "Entrez votre mail"})
    password = PasswordField('Mot de passe', validators=[DataRequired()], render_kw={"placeholder": "Entrez votre mot de passe"})
    connexion = SubmitField("Se connecter")

class SignUpForm(FlaskForm):
    name = StringField("Nom d'utilistaeur", validators=[DataRequired(), Length(min = 2, max = 20)], render_kw={"placeholder": "Entrez votre nom"})
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "Entrez votre adresse e-mail"})
    password = PasswordField('Mot de passe', validators=[DataRequired()], render_kw={"placeholder": "Entrez un mot de passe"})
    connexion = SubmitField("S'inscrire")

class addForm(FlaskForm):
    name = StringField("Nom du produit", validators=[DataRequired()], render_kw={"placeholder": "Nom du produit"})
    price = StringField("Nom du produit", validators=[DataRequired()], render_kw={"placeholder": "Entrer le prix"})
    description = StringField("Nom du produit", validators=[DataRequired()], render_kw={"placeholder": "description"})
    quantite = StringField("Quantié", validators=[DataRequired()], render_kw={"placeholder": "Quantié"})
    img = FileField('Ajouter une photo')
    addp = SubmitField('Ajouter')
    
class AdminLogin(FlaskForm):
    user_name = StringField("Nom d'utilistaeur", validators=[DataRequired(), Length(min = 2, max = 20)], render_kw={"placeholder": "Nom d'utilisateur "})
    password = PasswordField('Mot de passe', validators=[DataRequired()], render_kw={"placeholder": "Entrez votre mot de passe"})
    connexion = SubmitField("Se connecter")

class AdminSign(FlaskForm):
    user_name = StringField("Nom d'utilistaeur", validators=[DataRequired(), Length(min = 2, max = 20)], render_kw={"placeholder": "Entrez votre nom d'utilisateur"})
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "Entrez votre adresse e-mail"})
    password = PasswordField('Mot de passe', validators=[DataRequired()], render_kw={"placeholder": "Entrez un mot de passe"})
    img = FileField('Photo de profil')
    connexion = SubmitField("S'inscrire")

class Update(FlaskForm):
    name = StringField("Nom du produit", validators=[DataRequired()], render_kw={"placeholder": "Nouveau nom du produit"})
    price = StringField("Nom du produit", validators=[DataRequired()], render_kw={"placeholder": "Nouveau prix prix"})
    description = StringField("Nom du produit", validators=[DataRequired()], render_kw={"placeholder": "Nouvelle description"})
    quantite = StringField("Quantié", validators=[DataRequired()], render_kw={"placeholder": "Quantié"})
    img = FileField('Nouvelle photo')
    addp = SubmitField('Appliquer la mise a jour')

    