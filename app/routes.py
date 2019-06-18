# -*- coding: utf-8 -*-
import os, datetime
from app import app, db
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.forms import PostForm, LoginForm
from app.models import Post, Picture, Admin
from flask_uploads import UploadSet, IMAGES



UPLOAD_FOLDER = 'app/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    query = db.session.query(Post)
    posts = query.all()[-3::]
    posts = posts[::-1]
    return render_template("index.html", posts = posts)

@app.route('/news')
@app.route('/news/<int:page>')
def news(page):
    posts = db.session.query(Post).paginate(page,9,False)
    return render_template("news.html", posts = posts)

@app.route('/article')
@app.route('/article/<newspage>')
def article(newspage):
    post = db.session.query(Post).get(newspage)
    return render_template('article.html', post=post)

@app.route('/gallery')
@app.route('/gallery/<int:page>')
def gallery(page):
    pictures = db.session.query(Picture).paginate(page,12,False)
    return render_template("gallery.html", pictures=pictures)

@app.route('/posting', methods=['GET', 'POST'])
def posting():
    form = PostForm()
    if request.method == 'POST':
        file = request.files['file']
        url = os.path.join('uploads/', file.filename)
        if file and (file.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__():
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER+filename)
            url = os.path.join('uploads/', filename)
        today = datetime.datetime.today().strftime("%Y.%m.%d %H:%M")
        post = Post(Title=form.title.data, Description=form.description.data, post=form.post.data, photo=url, date=today)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for("posting.html", form=form))
    return render_template("posting.html", form=form)

@app.route('/add_picture', methods=['GET', 'POST'])
def add_picture():
    form = PostForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and (file.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__():
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER+filename)
            url = os.path.join('uploads/',filename)
        today = datetime.datetime.today().strftime("%Y.%m.%d %H:%M")
        post = Picture(Title=form.title.data, photo=url, date=today)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for("add_picture", form=form))
    return render_template("gallery_add.html", form=form)

@app.route('/static/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/delete/<int:ident>/<page>')
def delete(ident, page):
    Post.query.filter(Post.id == ident).delete()
    db.session.commit()
    return redirect(url_for(page))