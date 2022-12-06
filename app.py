# pylint: disable=no-member

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_alchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    profile = db.relationship("Profile", backref="user", uselist=False)

    def __str__(self):
        return self.name


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __str__(self):
        return self.name


@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    users = User.query.all()  # select * from users
    return render_template('users.html', users=users)


@app.route('/user/<int:id>')
@login_required
def unique(id):
    user = User.query.get(id)  # select * from users
    return render_template('user.html', user=user)


@app.route('/user/delete/<int:id>')
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User()
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])
        # user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout(id):
    logout_user()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
