import os

from flask import Flask
import flask
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask import Flask, session
from flask_session import Session
from flask import jsonify, render_template, request, redirect, url_for
from channel import Channel
from chat_message import Message

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# A set of dictionaries to store the channel information, 1 for public channels and another for private channels and
# a global map of channel-id to channel mapping
# Channel id's have a unique id across public/private
public_channel_map = {}
global_channel_id_map = {}
private_channel_map = {}


# redirect the user to the login page if no user session is currently active
@app.before_request
def do_something_whenever_a_request_comes_in():
    if not 'username' in session and flask.request.method == 'GET':
        return render_template("index.html")


# default route for the server startup. Get request is only used when the user opens the index page directly on the browser
@app.route("/", methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        session['username'] = username
        session['email'] = email
        private_channel_map[username] = dict()
        return redirect(url_for('public_channels'))
    else:
        return render_template("index.html")


# route configuration for all the private channels created by the user.
@app.route("/private-channels")
def private_channels():
    username = session['username']
    if len(private_channel_map) > 0 and private_channel_map[username] and len(private_channel_map[username]) > 0:
        return render_template("channels.html", username=session['username'], channel_type='private',
                               channels=private_channel_map[username].values())
    else:
        msg = "No private channels found."
        return render_template("channels.html", username=session['username'], channel_type='private', message=msg)


# route configuration for all the private channels created by the user.
@app.route("/public_channels")
def public_channels():
    if len(public_channel_map) > 0:
        return render_template("channels.html", username=session['username'], channel_type='public',
                               channels=public_channel_map.values())
    else:
        msg = "No public channels found."
        return render_template("channels.html", username=session['username'], channel_type='public', message=msg)


# post api configured for creation of channels. This api is called for creation of both public and private channels.
# if a public/private channel already exists with a name it returns back an error messgae
@app.route("/create_channel", methods=['POST'])
def create_channel():
    # Get request level parameters
    channel_name = request.form.get("channel_name")
    channel_description = request.form.get("channel_description")
    channel_type = request.form.get("channel_type")
    username = session['username']
    # if the intent is to create private channel
    if 'public' == channel_type:
        # if a publoc channel with the given name already exists.
        if (channel_name in public_channel_map):
            msg = f"Public Channel with name {channel_name} already exists"
            return render_template("channels.html", username=username, channel_type='public',
                                   channels=public_channel_map.values(), error_message=msg)
        else:
            # create a new public channel and it to both the maps storing public channel information
            new_chanel = Channel(channel_name, username, channel_description, channel_type)
            public_channel_map[channel_name] = new_chanel
            global_channel_id_map[str(new_chanel.id)] = new_chanel
            msg = f"Public channel with name {channel_name} successfully created"
            return render_template("channels.html", username=username, channel_type='public',
                                   channels=public_channel_map.values(), message=msg)
    else:
        # Code to create a private channel

        # if user already has a private channel with the specified name, return an error message
        if len(private_channel_map) > 0 and private_channel_map[username] \
                and channel_name in private_channel_map[username]:
            msg = f"Private Channel with name {channel_name} already exists"
            return render_template("channels.html", username=session['username'], channel_type='private',
                                   channels=private_channel_map[username].values(), error_message=msg)
        else:
            # create a new private channel and it to both the maps storing private channel information
            new_chanel = Channel(channel_name, session['username'], channel_description, channel_type)
            private_channel_map[username][channel_name] = new_chanel
            global_channel_id_map[str(new_chanel.id)] = new_chanel
            msg = f"Public channel with name {channel_name} successfully created"
            return render_template("channels.html", username=session['username'], channel_type='private',
                                   channels=private_channel_map[username].values(), message=msg)


# api to connect to any private/public channel, if the channel_id and channel_channel_type are valid,
# it will return all the exisiting messages for the channel. channel_type can be used to add future validation to the project
@app.route("/connect_channel")
def connect_channel():
    channel_id = str(request.args.get("channel_id"))
    channel_type = request.args.get("channel_type")
    username = session['username']
    # Code to handle lookup for public channel
    if 'public' == channel_type:
        messages = global_channel_id_map[channel_id].circularQueue.as_list()
        msg = ''
        if len(messages) < 1:
            print('3333')
            msg = f"There are currently no messages in channel {global_channel_id_map[channel_id].channel_name}"
            print(msg)
        return render_template("chat_channel.html", username=username, channel_type='public',
                               messages=messages, error_message=msg,
                               channel_name=global_channel_id_map[channel_id].channel_name, channel_id=channel_id)

    else:
        # Code to handle lookup for public channel
        messages = global_channel_id_map[channel_id].circularQueue.as_list()
        msg = ''
        if len(messages) < 1:
            msg = f"There are currently no messages in channel {global_channel_id_map[channel_id].channel_name}"
        return render_template("chat_channel.html", username=username, channel_type='private',
                               messages=messages, error_message=msg,
                               channel_name=global_channel_id_map[channel_id].channel_name, channel_id=channel_id)


# api to add the message to a queue, if the queue is full, the oldest message is taken out from the queue
def add_to_queue(circularQueue, new_message):
    if circularQueue.isFull():
        circularQueue.dequeue()
    circularQueue.enqueue(new_message)


# socket handler to listen to any new messages sent by the client.
@socketio.on("send message")
def vote(data):
    message = data["message"]
    channel_id = data['channel_id']
    channel_type = data['channel_type']
    channel_name = data['channel_name']
    username = data['username']
    # Create a new message object and add it the global queue
    new_message = Message(username, channel_id, channel_name, message)
    add_to_queue(global_channel_id_map[channel_id].circularQueue, new_message)
    emit("new message", new_message.toDict(), room=channel_id)


# socket handler when a new join request is recieved for a channel
@socketio.on('join')
def on_join(data):
    channel_id = data['channel_id']
    channel_type = data['channel_type']
    global_channel_id_map[channel_id].user_count += 1
    total_user_count = global_channel_id_map[channel_id].user_count
    join_room(channel_id)
    emit('user count updated', {'total_user_count': str(total_user_count)}, room=channel_id)
