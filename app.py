from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Post.sqlite3'
app.secret_key = 'KEK'

db = SQLAlchemy(app)


@app.route('/')
def index():
    from models import Post
    return render_template('index.html',
                           posts=Post.query.filter(Post.parent_id == None).order_by(desc(Post.created_at)).all())


@app.route('/<int:id>/', methods=('GET', 'POST'))
def view(id):
    from models import Post
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
        from models import Post
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
    from models import Post
    print(Post.query.filter((Post.id == id) | (Post.parent_id == id)).delete())
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
