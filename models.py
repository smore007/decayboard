from manage import db, app


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    media_url = db.Column(db.String(255))
    body = db.Column(db.String(4096))

    def __init__(self, body, media_url=None, parent_id=None):
        self.body = body
        self.media_url = media_url
        self.parent_id = parent_id
