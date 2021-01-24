from manage import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    media_url = db.Column(db.String(255))
    title = db.Column(db.String(128))
    body = db.Column(db.String(4096))

    def __init__(self, title=None, body=None, media_url=None, parent_id=None):
        self.title = title
        self.body = body
        self.media_url = media_url
        self.parent_id = parent_id
