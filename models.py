from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __repr__(self):
        return f'{self.id} - {self.username}'


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=True)

    def __repr__(self):
        return f'{self.id}'
    
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey('chats.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    message = db.Column(db.String())
    chat = db.relationship('Chat', backref='chat_messages', foreign_keys=[chat_id])
    username = db.relationship('User', backref='user_messages', foreign_keys=[user_id])

    def __repr__(self):
        return f'{self.id} - {self.chat} - {self.username} - {self.message}'