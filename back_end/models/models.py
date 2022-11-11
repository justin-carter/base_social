import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    score = db.Column(db.BigInteger, default=0)
    created = db.Column(db.DateTime, server_default=db.func.now())
    modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True,)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text)
    pos_reaction = db.Column(db.Integer, default=0)
    neg_reaction = db.Column(db.Integer, default=0)
    report_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, server_default=db.func.now())
    modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    comment = db.Column(db.Text, nullable=False)
    pos_reaction = db.Column(db.Integer, default=0)
    neg_reaction = db.Column(db.Integer, default=0)
    report_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, server_default=db.func.now())
    modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Reaction(enum.Enum):
    POSITIVE = 'pos'
    NEGATIVE = 'neg'


class UserPostReact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    reaction = db.Column(db.Enum(Reaction, values_callable=lambda x: [str(member.value) for member in Reaction]))
    created = db.Column(db.DateTime, server_default=db.func.now())
    modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
