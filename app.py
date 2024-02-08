from flask import Flask, render_template, redirect, url_for, flash, request, session
from forms import LoginForm, SignUpForm, addForm, AdminLogin, AdminSign, Update
from flask_migrate import Migrate
from models import db, User, Produits, Admin
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = "0D@nZ0kA$h%k%-6"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
db.init_app(app)
migrate = Migrate(app, db) 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    produits = Produits.query.order_by(Produits.id.desc()).limit(3).all()
    user_email = session.get('user_email')

    return render_template('index.html', produit = produits, user_email = user_email)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    logout_user()
    return redirect(url_for('index'))

@app.route("/logoutadmin", methods = ["GET", "POST"])
def logoutadmin():
    session.pop('user_name', None)
    session.pop('user_photo', None)
    return redirect(url_for('adLog'))

@app.route("/shop")
def shop():
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    liste = Produits.query.all()
    user_email = session.get('user_email')
    return render_template('shop.html', liste = liste, user_email = user_email)

@app.route("/about")
def about():
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    user_email = session.get('user_email')
    return render_template('about.html', user_email = user_email)

@app.route("/shopeo")
def shop_only():
    return render_template('shoponly.html')

@app.route("/service")
def service():
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    user_email = session.get('user_email')
    return render_template('service.html', user_email = user_email)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    if 'user_id' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        mail = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by( add_mail = mail ).first()

        if user and bcrypt.check_password_hash(user.mot_passe, password):
            login_user(user)

            session['user_id'] = user.id
            session['user_email'] = user.add_mail

            return redirect(url_for('index'))
        else:
            flash("Email ou mot de passe incorrect !")
            return redirect(url_for('login'))

    return render_template('login.html', form = login_form )

@app.route("/SignUp", methods=["GET", "POST"])
def Signup():
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    if 'user_id' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('index'))
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        nom = signup_form.name.data
        email = signup_form.email.data
        password = signup_form.password.data
        pw_hash = bcrypt.generate_password_hash(password)
        new_user = User(nom_user = nom, add_mail = email, mot_passe = pw_hash)
        print(new_user)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('Signup.html', form = signup_form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/add", methods = ['GET', 'POST'])
def add_product():
    user_name = session.get('user_name')
    user_photo = session.get('user_photo')
    add_form = addForm()
    if add_form.validate_on_submit():
        name = add_form.name.data
        price = add_form.price.data
        desc = add_form.description.data
        quant = add_form.quantite.data
        admin = Admin.query.filter_by(user_name=user_name).first()
        file = add_form.img.data
        UPLOAD_FOLDER = '/static/images'

        if file.filename == '':
            flash('Choisir une photo')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product = Produits(nom = name, prix = price, description = desc, quantite = quant, admin = admin, photo = filename)

        print(new_product)

        db.session.add(new_product)
        db.session.commit()

        flash("Produit ajoutée")

    return render_template('add.html', form = add_form, user_name = user_name, user_photo = user_photo)

@app.route("/AdLog", methods = ['GET', 'POST'])
def adLog():
    ad_log = AdminLogin()
    if ad_log.validate_on_submit():
        name = ad_log.user_name.data
        passe = ad_log.password.data

        login = Admin.query.filter_by( user_name = name ).first()
        if login and bcrypt.check_password_hash(login.mot_passe, passe):

            session['user_name'] = login.user_name
            session['user_photo'] = login.photo

            return redirect(url_for('adpan'))
        else:
            flash("Mot de passe ou nom d'utilisateur incorrect")
            return redirect(url_for('adLog'))
        
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    if 'user_id' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('index'))

    return render_template('adminLogin.html', form = ad_log)

@app.route("/adpannel")
#@login_required
def adpan():
    liste = Produits.query.all()
    user_name = session.get('user_name')
    user_photo = session.get('user_photo')

    return render_template('adminpannel.html', liste = liste, user_name = user_name, user_photo = user_photo )

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    up_prod = Update()
    product = Produits.query.get_or_404(id)
    user_name = session.get('user_name')
    user_photo = session.get('user_photo')

    if up_prod.validate_on_submit():
        product.nom = up_prod.name.data
        product.prix = up_prod.price.data
        product.description = up_prod.description.data
        product.quantite = up_prod.quantite.data
        photo = up_prod.img.data
        UPLOAD_FOLDER = '/static/images'
        

        if  photo.filename == '':
            flash('Choisissez une photo')
            return redirect(request.url)
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.photo

        db.session.commit()
        return redirect(url_for('adpan'))

    return render_template('update.html', form = up_prod, product = product, user_name = user_name, user_photo = user_photo)

@app.route("/AdSign", methods = ['GET', 'POST'])
def AdSign():
    ad_sign = AdminSign()
    if 'user_name' in session:
        flash('Deconnectez vous avant !')
        return redirect(url_for('adpan'))
    if ad_sign.validate_on_submit():
        nom = ad_sign.user_name.data
        email = ad_sign.email.data
        passe = ad_sign.password.data
        pw_hash = bcrypt.generate_password_hash(passe)
        photo = ad_sign.img.data
        UPLOAD_FOLDER = '/static/images'
        

        if  photo.filename == '':
            flash('Choisissez une photo')
            return redirect(request.url)
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            admin = Admin(user_name = nom,  add_mail = email, mot_passe = pw_hash, photo = filename)

        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('adLog'))

    return render_template('adminSignup.html', form = ad_sign)

@app.route("/usemanage")
def usemanage():
    liste = User.query.all()

    user_name = session.get('user_name')
    user_photo = session.get('user_photo')

    return render_template('usersmanage.html', liste = liste, user_name = user_name, user_photo = user_photo)

@app.route("/delpro/<int:id>/")
def delpro(id):
    liste = Produits.query.get_or_404(id)

    db.session.delete(liste)
    db.session.commit()
    return redirect(url_for('adpan'))

@app.route("/deluse/<int:id>/")
def deluse(id):
    liste = User.query.get_or_404(id)

    db.session.delete(liste)
    db.session.commit()
    return redirect(url_for('usemanage'))

@app.route("/show/<int:id>/")
def show(id):
    return redirect(url_for('shoponly', id = id))

@app.route("/shop_only/<int:id>/")
def shoponly(id):
    liste = Produits.query.get_or_404(id)
    user_email = session.get('user_email')
    return render_template('shoponly.html', liste = liste, user_email = user_email)
    
@app.route("/rdv")
def rdv():
    user_email = session.get('user_email')
    if 'user_email' in session:
        redirect(url_for('rdv'))
    else:
        flash("Veuillez d'abord vous connecter à votre compte !")
        return redirect(url_for('login'))
    return render_template('rdv.html', user_email = user_email)