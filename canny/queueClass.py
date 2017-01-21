class Queue():
    """
        Implementation of a queue (FIFO) data structure to be used
        specifically for storing co-ordinates.

        NB: no rear pointer is needed since there is no limit on memory
        (technically, there is, but the Queue will never reach that size)

        NB: no front pointer is needed since python handles this itself -
        when the first element is removed, the next element is now the front
        of the queue automatically
    """

    def __init__(self):
        # Initialise elements of queue
        self.elements = []

    def __str__(self):
        # Initialise output sString
        outputString = ''

        # Convert each element into a co-ordinate representation and
        # append to outputString
        for i in range(self.pointer,len(self.elements)+1):#test this
            element = elements[i]
            outputString += '('+str(element[0])+','+str(element[1])+'), '

        return outputString

    def enqueue(self,val):
        # Add the new value to the queue
        self.elements.append(val)

    def dequeue(self):
        # Remove and return the first element of the queue
        return self.elements.pop(0)

    def isEmpty(self):
        # If the length of the elements list is 0, it's empty
        return len(self.elements) == 0

