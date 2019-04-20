# server.py
"""
    For here, the server will run in a loop, processing requests one at a time, receive the message, perform the error
    check, and tell the client if the message was received successfully or not while printing out the results to its
    own terminal window. After that all works, we can implement an argument that will enable a occasional bit flipping.
"""

import socket, sys
from random import *

# an enum might be a good structure to do a "switch" statement (doesn't technically exist in python, so if-elif-else)
# feel free to implement whatever you prefer if an enum is too complicated
from enum import Enum


def create_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def make_switch(message, size):
    random_int = random()
    bit_num = random(1, size)
    if random_int < 0.5:
        if message[bit_num] == 1:
            message[bit_num] = 0
        else:
            message[bit_num] = 1
    return message


# define the different error checking functions here
def parity_1D(message, arg):
    # initialize a list that will contain the parity bit for each segment
    parity_bit_list = []
    # iterate through each segment
    for index, segment in enumerate(segmented_message):

        parity_count = 0
        # iterate through the message one bit at a time, and increment the parity_count every time a 1 is encountered
        for bit in segment:
            if bit == '1':
                parity_count += 1

        # compute the parity bit based on the parity schema
        if arg == 'even':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 1
            else:
                parity_bit = 0

        elif arg == 'odd':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 0
            else:
                parity_bit = 1

        else:
            sys.exit('\nTYPE PARITY1D ARG ERROR: valid args -> even, odd')

        # append the parity bit to the list at the same index
        parity_bit_list.append(str(parity_bit))

        # add the parity bit to the end of each segment in the message
        segmented_message[index] += parity_bit_list[index]

    return segmented_message


# 2D parity check
def parity_2D(message, arg):
    row_parity_bit_list = []

    # iterate through each segment
    for index, segment in enumerate(segmented_message):

        parity_count = 0
        # iterate through the message one bit at a time, and increment the parity_count every time a 1 is encountered
        for bit in segment:
            if bit == '1':
                parity_count += 1

        # compute the parity bit based on the parity schema
        if arg == 'even':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 1
            else:
                parity_bit = 0

        elif arg == 'odd':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 0
            else:
                parity_bit = 1

        else:
            sys.exit('\nTYPE PARITY1D ARG ERROR: valid args -> even, odd')

        # append the parity bit to the list at the same index
        row_parity_bit_list.append(str(parity_bit))

        # add the parity bit to the end of each segment in the message
        segmented_message[index] += row_parity_bit_list[index]

    # create a list containing representations of each column of bits for the column check
    columns = [''.join(b) for b in zip(*segmented_message)]

    # initiallize a string to store these bits since it will just be appended to the end of the segmented message
    column_parity_bits = ''

    # perform the parity check on the columns
    for index, segment in enumerate(columns):

        parity_count = 0
        # iterate through the message one bit at a time, and increment the parity_count every time a 1 is encountered
        for bit in segment:
            if bit == '1':
                parity_count += 1

        # compute the parity bit based on the parity schema
        if arg == 'even':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 1
            else:
                parity_bit = 0

        elif arg == 'odd':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 0
            else:
                parity_bit = 1

        else:
            sys.exit('\nTYPE PARITY1D ARG ERROR: valid args -> even, odd')

        # append the parity bit to the list at the same index
        column_parity_bits += str(parity_bit)

    # append the column string to the segmented message
    segmented_message.append(column_parity_bits)

    return segmented_message


# cyclic redundancy check
def crc(message, arg):
    # need to figure out a way to pass in the polynomial if the user is going to specify that
    # otherwise we can just use a default one
    pass


# checksum, perhaps summing the message in 8-bit pieces?
def checksum(message, arg):
    # if the message is only one segment long, just flip it
    if len(segmented_message) < 2:
        checksum = ones_complement(segmented_message[0])
    else:
        # iterate through the message and sum the binary values together
        sum = int(segmented_message[0], 2)
        for i in range(1, len(segmented_message)):
            sum += int(segmented_message[i], 2)

            # deal with the wraparound bit if it exists
            if len('{0:b}'.format(sum)) > 8:
                sum += 1

        checksum = '{0:b}'.format(sum)
        # one's complement the sum for the checksum
        checksum = ones_complement(checksum)

    segmented_message.append(checksum)

    return segmented_message


def ones_complement(binary_string):

    flipped_string = ''

    for bit in binary_string:

        if bit == '0':
            flipped_bit = 1
        else:
            flipped_bit = 0

        flipped_string += str(flipped_bit)

    return flipped_string

# compare the received message to the server-checked message
# send a message to the client if the message was received correctly


def compare_messages(received_message, error_checked_message):
    if received_message == error_checked_message:
        print("Message was received correctly. Message is " + error_checked_message)
    else:
        print("Message receiving failed. Messaged received is " + error_checked_message)


# break up the message into a list of 8 bit binary string segments for processing
def segment(message):
    # create a list of 8 bit segments of the message, in order
    # we start the for loop at 2 to skip over the '0b' prefix that begins every binary string representation in python
    segment_list = ([bin(message)[n:n + 8] for n in range(2, len(bin(message)), 8)])
    return segment_list


if __name__ == '__main__':
    # write the loop and order of program execution here
    what_loop = 1
    while True:
        try:
            sent = conn.recv(2048).split(", ")
            message = sent[0].bin()
            segmented_message = segment(message)
            error_type = sent[1]
            arg2 = sent[2]
            print(message)
            size = message.length
            error_message = make_switch(message, size)
            if error_type == "1d parity":
                error_checked_message = parity_1D(error_message, arg2)
                compare_messages(message, error_checked_message)
            elif error_type == "2d parity":
                error_checked_message = parity_2D(message, arg2)
                compare_messages(message, error_checked_message)
            elif error_type == "crc":
                error_checked_message = crc(message, arg2)
                compare_messages(message, error_checked_message)
            else:
                error_checked_message = checksum(message, arg2)
                compare_messages(message, error_checked_message)

        except:
            continue
