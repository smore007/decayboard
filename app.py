from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyxznyonpytfnf:6a05f4e3f7997bd3f4c1f995f7f0fae3d28d4202b8294212fbbc22d1379e737a@ec2-52-23-86-208.compute-1.amazonaws.com:5432/d5a8pr2slh4f23'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def get_posts(parent_id=None):
    return Post.query.filter(Post.parent_id is parent_id).all()


@app.route('/')
def index():
    return render_template('index.html', posts=get_posts())


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        p = Post(title=title, body=body)

        db.session.add(p)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')


if __name__ == '__main__':
    app.run()
