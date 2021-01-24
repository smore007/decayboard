from flask import Flask, render_template, request
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)


def get_posts(parent_id=None):
    from . import db
    return db.Post.query.filter(db.Post.parent_id is parent_id).all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', posts=get_posts())


if __name__ == '__main__':
    app.run()
