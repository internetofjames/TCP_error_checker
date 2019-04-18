# client.py
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
                        type=str, nargs=2, required=False,
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

    # call error checking function (i.e. parity_1D) depending on argparser value
    # these functions return the appropriate binary error code, which this function will return
    if args.type[0] == 'parity1d':
        error_checked_message = parity_1D(segmented_message)

    elif args.type[0] == 'parity2d':
        error_checked_message = parity_2D()

    elif args.type[0] == 'crc':
        error_checked_message = crc()

    elif args.type[0] == 'checksum':
        error_checked_message = checksum()

    else:
        # invalid arg provided: exit program with message
        sys.exit('\nTYPE ARG ERROR: valid args -> parity1d, parity2d, crc, checksum')

    return error_checked_message


# 1D parity check
def parity_1D(segmented_message):

    # initialize a list that will contain the parity bit for each segment
    parity_bit_list = []

    print(segmented_message)

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
def parity_2D():
    pass


# cyclic redundancy check
def crc():
    # need to figure out a way to pass in the polynomial if the user is going to specify that
    # otherwise we can just use a default one
    pass


# checksum, perhaps summing the message in 8-bit pieces?
def checksum():
    pass


""" Message processing and printing functions """

# break up the message into a list of 8 bit binary string segments for processing
def segment(message):
    # create a list of 8 bit segments of the message, in order
    # we start the for loop at 2 to skip over the '0b' prefix that begins every binary string representation in python
    segment_list = ([bin(message)[n:n + 8] for n in range(2, len(bin(message)), 8)])
    return segment_list


# print the message in groupings so it is easier to read
def print_message(segmented_message):
    # process the message and error_code ints as binary numbers (without the 0b prefix) and convert to a string,
    # spaced by every 8 bits
    message_string = ' '.join([n for n in segmented_message])

    # some formatting for a nice print out of the message
    print('\n{} {}'.format(args.type[0], args.type[1]))
    print('\nMessage')
    print('-' * len(message_string))
    print(message_string)


""" Server communication functions """
# implement functions for connecting to, sending data, and receiving data from the server here


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = setup_argparser(parser)

    message = generate_message(args.bits)
    new_message = error_check(message)
    print_message(new_message)

    # pretty_print_message(message, error_code)

