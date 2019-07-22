# This is a class for a bounded 100 message queue. This has been taken from github https://gist.github.com/computinginschools/ac50bc81a43b7302cefda4132062eb5a
# and modified to add support for returning a list of messages in the queue in the timebased insertion order.

class CircularQueue(object):
    ''' Simple circular queue '''

    def __init__(self, max):
        ''' Initialise the queue '''
        # Define instance variables
        self.__frontPointer = 0
        self.__rearPointer = max - 1
        self.__size = 0
        self.__max = max

        # Initialise empty queue
        self.queue = []
        for i in range(self.__max):
            self.queue.append('')

    def __str__(self):  # Print magic method
        ''' Print raw queue '''
        string = '\n'
        for i in range(self.__max):
            string += '{!s:3}'.format(i) + ' : ' + str(self.queue[i]) + '\n'
        string += '\n'
        string += 'Front Pointer : ' + str(self.__frontPointer) + '\n'
        string += 'Rear Pointer  : ' + str(self.__rearPointer) + '\n'
        string += 'Size          : ' + str(self.__size) + '\n'
        return string

    def __isEmpty(self):
        ''' Check whether queue is empty '''
        return self.__size == 0

    def isFull(self):
        ''' Check whether queue is full '''
        return self.__size == self.__max

    def enqueue(self, item):
        ''' Enqueue item, if space '''
        if self.isFull():
            return False
        else:
            self.__rearPointer = (self.__rearPointer + 1) % self.__max
            self.queue[self.__rearPointer] = item
            self.__size += 1

    def dequeue(self):
        ''' Dequeue item, if one exists '''
        if self.__isEmpty():
            return False
        else:
            dequeued = self.queue[self.__frontPointer]
            self.queue[self.__frontPointer] = ''
            self.__frontPointer = (self.__frontPointer + 1) % self.__max
            self.__size -= 1
            return dequeued

    def peek(self):
        ''' Peek at head of list '''
        if self.__isEmpty():
            return False
        else:
            return self.queue[self.__frontPointer]

    def as_list(self):
        ret_list = []
        if self.__size == 0:
            return ret_list
        rear_modulo = self.__rearPointer % self.__max
        front_modulo = self.__frontPointer % self.__max
        if (rear_modulo > front_modulo):
            return self.queue[front_modulo:rear_modulo + 1]
        else:
            if (self.__size == 1 and rear_modulo == front_modulo == 0):
                ret_list.append(self.queue[0])
            else:
                for y in range(front_modulo, self.__max):
                    ret_list.append(self.queue[y])
                for x in range(0, rear_modulo + 1):
                    ret_list.append(self.queue[x])

            return ret_list
