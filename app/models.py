from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), index = True)
    Description = db.Column(db.String(256), index = True)
    post = db.Column(db.String(10000), index = True)
    photo = db.Column(db.String(80))
    date = db.Column(db.String(80))

    def __repr__(self):
        repr = {"title":self.Title, "description":self.Description, "post":self.post}
        return repr

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), index = True)
    photo = db.Column(db.String(80))
    date = db.Column(db.String(80))

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))