"""
    I'm thinking the client should be ran a single instance at a time, exiting and closing the socket after sending message and receiving validation or not
"""

import socket, random
import sys, argparse


# function sets up the argparser arguments for the program
def setup_argparser(parser):
    # change required to true when socket connection function is project-ready
    parser.add_argument('-p', '--port', type=int, required=False, help='Usage: -p or --port <portNumber>')
    parser.add_argument('-b', '--bits', type=int, required=True, help='Usage: -b or --bits <numberOfBits>')
    parser.add_argument('-t', '--type',
                        type=str, nargs=2, required=True,
                        help='Usage: -t or --type <typeOfErrorCheck> <option>'
                        ) # type flag accepts two arguments, the name of the error check and a schema (i.e. parity1d even)
    args = parser.parse_args()
    return args


# return a random integer of num_bits bits long
def generate_message(num_bits):
    return random.getrandbits(num_bits)


""" Error check code generation functions """


# pass the segmented message list to the appropriate error checking function
def error_check(message):

    segmented_message = segment(message)

    print(segmented_message)

    # call error checking function (i.e. parity_1D) depending on argparser value
    # these functions return the appropriate binary error code, which this function will return
    if args.type[0] == 'parity1d':
        error_checked_message = parity_1D(segmented_message)

    elif args.type[0] == 'parity2d':
        error_checked_message = parity_2D(segmented_message)

    elif args.type[0] == 'crc':
        error_checked_message = crc(message)
        error_checked_message = segment(int(error_checked_message, 2))

    elif args.type[0] == 'checksum':
        error_checked_message = checksum(segmented_message)

    else:
        # invalid arg provided: exit program with message
        sys.exit('\nTYPE ARG ERROR: valid args -> parity1d, parity2d, crc, checksum')

    return error_checked_message


# 1D parity check
def parity_1D(segmented_message):

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
        if args.type[1] == 'even':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 1
            else:
                parity_bit = 0

        elif args.type[1] == 'odd':
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
def parity_2D(segmented_message):

    row_parity_bit_list = []

    # iterate through each segment
    for index, segment in enumerate(segmented_message):

        parity_count = 0
        # iterate through the message one bit at a time, and increment the parity_count every time a 1 is encountered
        for bit in segment:
            if bit == '1':
                parity_count += 1

        # compute the parity bit based on the parity schema
        if args.type[1] == 'even':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 1
            else:
                parity_bit = 0

        elif args.type[1] == 'odd':
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
        if args.type[1] == 'even':
            if parity_count % 2 == 1:  # parity_count is odd
                parity_bit = 1
            else:
                parity_bit = 0

        elif args.type[1] == 'odd':
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
def crc(message):

    message = '{0:b}'.format(message)

    try:
        divisor = int(args.type[1], 2)  # will throw a ValueError if args.type[1] is not a binary string

        # add polynomial length - 1 zeros to the end of message
        zeros = '0' * (len(args.type[1]) - 1)
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


# checksum using 8 bit segments
def checksum(segmented_message):

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


""" Message processing and printing functions """

# break up the message into a list of 8 bit binary string segments for processing
def segment(message):
    # create a list of 8 bit segments of the message, in order
    # we start the for loop at 2 to skip over the '0b' prefix that begins every binary string representation in python
    segment_list = ([bin(message)[n:n + 8] for n in range(2, len(bin(message)), 8)])
    return segment_list


# I acknowledge the unary '~' operator, however without the ability to deal with unsigned ints in python, it doesn't
# # function correctly for our use case
def ones_complement(binary_string):

    flipped_string = ''

    for bit in binary_string:

        if bit == '0':
            flipped_bit = 1
        else:
            flipped_bit = 0

        flipped_string += str(flipped_bit)

    return flipped_string


# print the message in groupings so it is easier to read
def print_message(segmented_message):
    # process the message and error_code ints as binary numbers (without the 0b prefix) and convert to a string,
    # spaced by every 8 bits
    message = ''.join([n for n in segmented_message])
    segmented_message = segment(int(message, 2))
    message_string = ' '.join([n for n in segmented_message])

    # some formatting for a nice print out of the message
    print('\n{} {}'.format(args.type[0], args.type[1]))
    print('\nMessage')
    print('-' * len(message_string))
    print(message_string)


""" Server communication functions """
# implement functions for connecting to, sending data, and receiving data from the server here

# connect to the socket that the server is running on
def server_connect(port):
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = ('localhost', port)
    try:
        print('Connecting to server %s on port %s...' % connection)
        server_connection.connect()
    except:
        print('Connection failed, exiting...')
        server_connection.close()
        sys.exit()

    return server_connection


# concatenate the message to be sent to the server
# message format is: '<data>,<typeArg1>,<typeArg2>'
def prepare_message(segmented_data):
    data_string = ''.join([n for n in segmented_data])
    message = '{},{},{}'.format(data_string, args.type[0], args.type[1])
    return message


# send message to server
def send_message(connection, message):
    print('Sending message to %s' % connection.getpeername())
    connection.send(message.encode('utf-8'))


# receive server reply
def receive_reply(connection):
    reply = connection.recv(2048).decode('utf-8')
    return reply


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = setup_argparser(parser)

    data = generate_message(args.bits)
    segmented_data = error_check(data)
    print_message(segmented_data)

    # create socket and connect to server
    server_connection = server_connect(int(args.port))

    # prepare message to be sent to server
    message = prepare_message(segmented_data)

    # send message to server and receive reply
    send_message(server_connection, message)
    reply = receive_reply(server_connection)
