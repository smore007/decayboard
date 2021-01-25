from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from database import db
import database
from models import Post
from sqlalchemy import desc

app = Flask(__name__)
database.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nxytkuntklroyq:7e6e9d6b13d74757499a34c4774f2025b50e3d34fbdd102b2c7fa091ec9ceea6@ec2-54-82-208-124.compute-1.amazonaws.com:5432/d74lh90jcnvjl6'
app.secret_key = 'KEK'


@app.route('/')
def index():
    return render_template('index.html',
                           posts=Post.query.filter(Post.parent_id == None).order_by(desc(Post.created_at)).all())


@app.route('/<int:id>/', methods=('GET', 'POST'))
def view(id):
    if request.method == 'POST':
        body = request.form['body']

        if not body:
            flash("Body is required.")
        else:
            p = Post(body=body, parent_id=id)

            db.session.add(p)
            db.session.commit()

    return render_template('view.html',
                           posts=Post.query.filter((Post.id == id) | (Post.parent_id == id)).all())


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None
        if not title or not title.strip():
            error = "Title is required."
        elif not body or not body.strip():
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            p = Post(title=title, body=body)

            db.session.add(p)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('create.html')


@app.before_request
def load_admin():
    if session.get('is_admin'):
        g.is_admin = True
    else:
        g.is_admin = False


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if request.form['password'] == 'kek':
            session['is_admin'] = True
            return redirect(url_for('index'))
        else:
            flash('Incorrect password')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/<int:id>/delete')
def delete(id):
    print(Post.query.filter((Post.id == id) | (Post.parent_id == id)).delete())
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
