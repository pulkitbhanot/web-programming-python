# Class to model a channel object, it stores the details like id, owner, description, a reference to a circular queue
# with 100 messages and total number of join requests for the channel
from circular_queue import CircularQueue
import itertools


class Channel:
    newid = itertools.count()

    def __init__(self, channel_name, channel_owner, channel_description, channel_type):
        self.id = next(Channel.newid)
        self.channel_name = channel_name
        self.channel_owner = channel_owner
        self.channel_description = channel_description
        self.user_count = 0
        self.channel_type = channel_type
        self.circularQueue = CircularQueue(100)

    def __str__(self):
        string = '\n'
        string += 'Channel Name : ' + str(self.channel_name) + '\n'
        string += 'channel_owner : ' + str(self.channel_owner) + '\n'
        string += 'channel_description : ' + str(self.channel_description) + '\n'
        string += 'user_count : ' + str(self.user_count) + '\n'
        string += 'CircularQueue : ' + str(self.circularQueue) + '\n'
        return string
