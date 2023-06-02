import math
from collections import OrderedDict

class Node:
    def __init__(self, value=None, next=None, tf_idf=None, skip=None, tf = None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.tf = tf
        self.tf_idf = tf_idf
        self.next = next
        self.skip = skip

class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.node_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if (self.start_node is None):
            return
        else:
            node = self.start_node
            while(node is not None):
                    traversal.append(node.value)
                    node=node.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            #when skip length is less than or equal to 1
            if self.skip_length<=1:
                return traversal
            else:
                x = self.start_node
                while(x is not None):
                        traversal.append(x.value)
                        x=x.skip
            return traversal

    def add_skip_connections(self):
        n_skips = math.floor(math.sqrt(self.length))
        if (n_skips * n_skips == self.length):
            n_skips = n_skips - 1
        self.n_skips = n_skips
        self.skip_length = int(round(math.sqrt(self.length),0))
        """ Write logic to add skip pointers to the linked list.
            This function does not return anything.
            To be implemented."""
        h_skip = self.start_node
        h_next = self.start_node
        if (self.skip_length <= 1):
            return
        else:
            skips = self.n_skips
            while (skips>0):
                skips -= 1
                skip_length = self.skip_length
                while(skip_length>0):
                    skip_length -= 1
                    h_next = h_next.next
                h_skip.skip = h_next
                h_skip = h_skip.skip

    def insert_at_end(self, tf, value):
        n_node = Node(value=value, tf_idf=tf)
        self.length = self.length + 1
        node = self.start_node
        if(self.start_node is None):
            self.start_node = n_node
            self.end_node = n_node
            return
        elif(self.start_node.value >= value):
            self.start_node = n_node
            self.start_node.next = node
            return
        elif(self.end_node.value <= value):
            self.end_node.next = n_node
            self.end_node = n_node
            return
        else:
            while(node.value < value < self.end_node.value and node.next is not None):
                node = node.next
            a = self.start_node
            while(a.next != node and a.next is not None):
                a = a.next
            a.next = n_node
            n_node.next = node
        return