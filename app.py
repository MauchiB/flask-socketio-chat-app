from flask import Flask, redirect, render_template, request, flash, session, current_app, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from forms import LoginForm
from models import Message, Chat, User, db

app = Flask(__name__)
app.secret_key = 'erkmp;rwpwserjoprer'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chat.db')

socket = SocketIO(app, logger=True, engineio_logger=True)
csrf = CSRFProtect(app)
db.init_app(app)

'''First, log in to your account
   REGESTATION - /reg
   LOGIN - /login
   CHAT global - /chat
   CHAT local - /chat/room_id (if not, it is created)
   LOGOUT from account - /logout (if you login)
   CREATE DB - Flask --app app.py create
   DELETE DB - Flask --app app.py delete
   RUN - Flask --app app.py run --debug (if debug true)'''



@app.route('/', methods=['POST', 'GET'])
@app.route('/<room_id>')
def chat(room_id=None):
    if not session.get('user_id'):
        return redirect(url_for('reg'))
    room = room_id
    if not room:
        room = 'global_room'
    if session.get('user_id'):
        u = User.query.get(session.get('user_id'))
        if not Chat.query.filter_by(name=room).first():
            create_chat = Chat(name=room)
            db.session.add(create_chat)
            db.session.commit()
        chat = Chat.query.filter_by(name=room).first()
        if u:
            return render_template('chat.html', user=u.username, messages_room=Message.query.filter_by(chat=chat).all(), room=room)
    abort(404)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('user_id'): abort(404)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            flash('You login!')
            return redirect(url_for('chat'))
        flash('username or password not defind')
    return render_template('login.html', form=form)

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if session.get('user_id'): abort(404)
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
             flash('User already exists', 'error')
        else:
            u = User(username=form.username.data, password=form.password.data)
            db.session.add(u)
            db.session.commit()
        flash('You regestration account')
        return redirect(url_for('login'))
    return render_template('reg.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@socket.on('connect')
def connect(data):
    '''create connect to room'''
    room = request.args.get('room')
    username = request.args.get('username')
    join_room(room)
    send({'message':f'user {username} is joined in {room}'}, to=room)

@socket.on('disconnect')
def leave_room(data):
    '''leave room'''
    username = request.args.get('username')
    room = request.args.get('room')
    leave_room(room)
    send({'message:'f'user {username} left in the {room}'}, to=room)

@socket.on('send_message')
def message(data):
    '''Send message on room'''
    room = data['room']
    message = data['message']
    chat = Chat.query.filter_by(name=room).first()
    user = User.query.get(int(session.get('user_id')))
    m = Message(chat_id=chat.id, user_id=user.id, message=message)
    db.session.add(m)
    db.session.commit()
    emit('message_response', {'message':message, 'sender':user.username}, to=room)








@app.cli.command('create')
def create():
    with current_app.app_context():
        db.create_all()
        print('create')

@app.cli.command('delete')
def create():
    with current_app.app_context():
        db.drop_all()
        print('delete')


if __name__ == '__main__':
    socket.run(debug=True)