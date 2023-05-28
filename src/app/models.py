from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    name = db.Column(db.String(), nullable=False)
    uuid = db.Column(db.String(), nullable=False)

    def __init__(self, name):
        self.name = name
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"<User {self.id}, {self.name}, {self.uuid}>"


class AudioFile(db.Model):
    __tablename__ = "audio_files"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uuid = db.Column(db.String(), nullable=False)
    audio_data = db.Column(db.LargeBinary)

    def __init__(self, audio_data):
        self.uuid = str(uuid.uuid4())
        self.audio_data = audio_data

    def __repr__(self):
        return f"<User {self.id}, {self.name}, {self.uuid}>"
