# server.py
"""
    For here, the server will run in a loop, processing requests one at a time, receive the message, perform the error
    check, and tell the client if the message was received successfully or not while printing out the results to its
    own terminal window. After that all works, we can implement an argument that will enable a occasional bit flipping.
"""

import socket, sys

# an enum might be a good structure to do a "switch" statement (doesn't technically exist in python, so if-elif-else)
# feel free to implement whatever you prefer if an enum is too complicated
from enum import Enum


def create_socket():
    pass


# define the different error checking functions here

# compare the received message to the server-checked message
# send a message to the client if the message was received correctly
def compare_messages(received_message, error_checked_message):
    pass


if __name__ == '__main__':
    # write the loop and order of program execution here
    pass
