# Class to model a message in the application, it has the required details like sender username, channel id,
# time of message recieved on the server and message contents.
import time


class Message:

    # constructor for the object
    def __init__(self, sender_name, channel_id, channel_name, message_content):
        self.sender_name = sender_name
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.message_content = message_content
        self.message_time = str(time.ctime())

    # returns a string representation of the message
    def __str__(self):
        string = '\n'
        string += 'sender_name : ' + str(self.sender_name) + '\n'
        string += 'channel_name : ' + str(self.channel_name) + '\n'
        string += 'message_time : ' + str(self.message_time) + '\n'
        return string

    # returna a dictionary of the message details that is sent as the response to the user.
    def toDict(self):
        return {'sender_name': self.sender_name,
                'channel_id': self.channel_id,
                'channel_name': self.channel_name,
                'message_content': self.message_content,
                'message_time': self.message_time}
