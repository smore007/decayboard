import datetime
from database import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    parent_id = db.Column(db.Integer)
    media_url = db.Column(db.String(255))
    title = db.Column(db.String(128))
    body = db.Column(db.String(4096))

    def __init__(self, title=None, body=None, media_url=None, parent_id=None):
        self.title = title
        self.body = body
        self.media_url = media_url
        self.parent_id = parent_id


def create_post(title=None, body=None, media_url=None, parent_id=None):
    p = Post(title=title, body=body, media_url=media_url, parent_id=parent_id)
    db.session.add(p)
    db.session.commit()


