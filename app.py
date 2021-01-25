from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import os
from database import db
import database
import commands
from models import Post
from sqlalchemy import desc

# init flask
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# setup dependencies
database.init_app(app)
commands.init_app(app)


@app.route('/')
def index():
    return render_template('index.html',
                           posts=Post.query.filter(Post.parent_id == None).order_by(desc(Post.created_at)).all())


@app.route('/<int:id>/', methods=('GET', 'POST'))
def view(id):
    if request.method == 'POST':
        body = request.form['body']
        media_url = request.form['media_url']

        if not body:
            flash("Body is required.")
        else:
            p = Post(body=body, parent_id=id, media_url=media_url)

            db.session.add(p)
            db.session.commit()

            return redirect(url_for('view', id=id))  # fix for refresh resend

    return render_template('view.html',
                           posts=Post.query.filter((Post.id == id) | (Post.parent_id == id)).all())


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        media_url = request.form['media_url']

        error = None
        if not title or not title.strip():
            error = "Title is required."
        elif not body or not body.strip():
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            p = Post(title=title, body=body, media_url=media_url)

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


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    if g.is_admin:
        Post.query.filter((Post.id == id) | (Post.parent_id == id)).delete()
        db.session.commit()
        return redirect(request.args.get('next'))
    else:
        flash('You must be admin!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
