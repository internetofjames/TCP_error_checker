# server.py
"""
    For here, the server will run in a loop, processing requests one at a time, receive the message, perform the error
    check, and tell the client if the message was received successfully or not while printing out the results to its
    own terminal window. After that all works, we can implement an argument that will enable a occasional bit flipping.
"""

import socket, sys, random
import optparse


# function sets up the OptionParser option for the program
def setup_optparser(parser):
    # change required to true when socket connection function is project-ready
    parser.add_option('-f', '--flip', action='store_true',
                        help='Usage: Include -f or --flip to enable potential flipping of received message bits')
    options, args = parser.parse_args()
    return options

def make_switch(message, size):
    random_int = random()
    bit_num = random(1, size)
    if random_int < 0.5:
        if message[bit_num] == '1':
            message[bit_num] = '0'
        else:
            message[bit_num] = '1'
    return message


# define the different error checking functions here
def parity_1D(message, arg):
    segmented_message = segment(message)
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
    segmented_message = segment(message)
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

    # initialize a string to store these bits since it will just be appended to the end of the segmented message
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
    message = '{0:b}'.format(message)

    try:
        divisor = int(arg, 2)  # will throw a ValueError if args.type[1] is not a binary string

        # add polynomial length - 1 zeros to the end of message
        zeros = '0' * (len(arg) - 1)
        temp_message = message + zeros

        # because of how python represents binary, we can pad our divisor with trailing zeros for division
        divisor = '{0:b}'.format(divisor)
        divisor_padding = '0' * (len(temp_message) - len(divisor))
        divisor += divisor_padding

        # convert message and divisor to numbers for XOR division
        temp_message = int(temp_message, 2)
        divisor = int(divisor, 2)

        # perform the crc, using the length of the message padding (zeros) as the stopping condition for dividing
        stop_condition = False
        remainder = ''
        while not stop_condition:
            # shift the divisor to shorten it to the length of the message if it has changed
            shift_amount = len('{0:b}'.format(divisor)) - len('{0:b}'.format(temp_message))
            if shift_amount > 0:
                divisor = divisor >> shift_amount

            temp_message = temp_message ^ divisor
            remainder = '{0:b}'.format(temp_message)
            if len(remainder) <= len(zeros):
                stop_condition = True

        # if the remainder has leading 0's, python automatically omits those, so we need to re-prepend them to the crc code
        if len(remainder) < len(zeros):
            leading_zeros = '0' * (len(zeros) - len(remainder))
            remainder = leading_zeros + remainder

        # append the remainder to the message
        message += remainder
        print(remainder)

    except ValueError:
        sys.exit('\nTYPE PARITY1D ERROR: Invalid arg. Supply arg with valid binary polynomial (e.g. 1011)')

    return message


# checksum, perhaps summing the message in 8-bit pieces?
def checksum(message):
    segmented_message = segment(message)
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


def compare_messages(received_message, checked_message):
    if received_message == checked_message:
        print("Message was received correctly. Message is " + checked_message)
    else:
        print("Message receiving failed. Messaged received is " + checked_message)


# break up the message into a list of 8 bit binary string segments for processing
def segment(message):
    # create a list of 8 bit segments of the message, in order
    # we start the for loop at 2 to skip over the '0b' prefix that begins every binary string representation in python
    segment_list = ([bin(message)[n:n + 8] for n in range(2, len(bin(message)), 8)])
    return segment_list


if __name__ == '__main__':

    parser = optparse.OptionParser()
    options = setup_optparser(parser)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip_address = 'localhost'
    port = 9088
    server.bind((ip_address, port))
    print('Now serving on port %s' % port)
    server.listen(1)
    while True:
        try:
            conn, addr = server.accept()
            received = conn.recv(2048)
            received = received.decode('utf-8')
            received = received.split(',')
            message = received[0]
            error_type = received[1]
            error_arg2 = received[2]
            print(message)
            size = message.__len__()
            if options.flip:
                message = make_switch(message, size)
            if error_type == "parity1d":
                error_checked_message = parity_1D(message, error_arg2)
                compare_messages(message, error_checked_message)
            elif error_type == "parity2d":
                error_checked_message = parity_2D(message, error_arg2)
                compare_messages(message, error_checked_message)
            elif error_type == "crc":
                error_checked_message = crc(message, error_arg2)
                compare_messages(message, error_checked_message)
            else:
                error_checked_message = checksum(message)
                compare_messages(message, error_checked_message)
        except KeyboardInterrupt:
            conn.close()
            server.close()
            sys.exit()

    conn.close()
    server.close()
