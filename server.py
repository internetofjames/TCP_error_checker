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


# function to randomly flip a bit in the message
def make_switch(message, size):
    message_array = [c for c in message]  # python str type cannot have individual chars replaced through indexing, conversion to a list is necessary
    random_int = random.random()
    bit_num = random.randint(0, size-1)
    if random_int < 0.5:
        if message_array[bit_num] == '1':
            message_array[bit_num] = '0'
            print("Bit", bit_num, "was flipped.")

    else:
        print("No bits were flipped.")

    # convert back to string
    message = ''.join([i for i in message_array])

    return message


# define the different error checking functions here
def parity_1D(segmented_message, arg):

    # remove the parity bits from the received message for processing
    for i, s in enumerate(segmented_message):
        segmented_message[i] = s[0:(len(s) - 1)]

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
def parity_2D(segmented_message, arg):

    # remove the last segment of the message, which contains the column parity information
    segmented_message = segmented_message[0:(len(segmented_message) - 1)]

    # remove the parity bits from the rest of the message for processing
    for i, s in enumerate(segmented_message):
        segmented_message[i] = s[0:(len(s) - 1)]

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
    try:
        divisor = int(arg, 2)  # will throw a ValueError if args.type[1] is not a binary string
        remove_length = divisor.bit_length()
        message = message[:-remove_length]
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
def checksum(segmented_message):
    # if the message is only one segment long, just flip it
    if len(segmented_message) < 2:
        segmented_message = s[0:(len(s) - 1)]
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
        status = "Message was received correctly. Message is " + str(checked_message)
    else:
        status = "Message receiving failed. Messaged received is " + str(checked_message)
    print(status)
    return status


# break up the message into a list of n-bit binary string segments for processing
def segment(message, segment_size):
    # create a list of segment_size bit segments of the message, in order
    segment_list = ([message[n:n + segment_size] for n in range(0, len(message), segment_size)])
    return segment_list

# reassemble message segments into continuous string
def unsegment(segmented_message):
    message = ''.join([n for n in segmented_message])
    return message


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
            print('\nAwaiting next message...')
            conn, addr = server.accept()
            received = conn.recv(2048)
            received = received.decode('utf-8')
            print(received)
            received = received.split(',')
            message = received[0]
            error_type = received[1]
            error_arg = received[2]
            print(message)
            size = message.__len__()
            message = make_switch(message, size)
            if error_type == "parity1d":
                segmented_message = segment(message, 9)  # parity1d works in 8-bit segments with a parity bit appended to the end, so 9 bits per segment
                error_checked_message = parity_1D(segmented_message, error_arg)
                error_checked_message = unsegment(error_checked_message)
                reply = compare_messages(message, error_checked_message)
            elif error_type == "parity2d":
                segmented_message = segment(message, 9)  # parity2d works in 8-bit segments with a parity bit appended to the end, including the 8-bit column parity segment, so 9 bits per segment
                error_checked_message = parity_2D(segmented_message, error_arg)
                error_checked_message = unsegment(error_checked_message)
                reply = compare_messages(message, error_checked_message)
            elif error_type == "crc":
                error_checked_message = crc(message, error_arg)
                reply = compare_messages(message, error_checked_message)
            else:
                error_checked_message = checksum(segmented_message)
                error_checked_message = unsegment(error_checked_message)
                reply = compare_messages(message, error_checked_message)

            reply = reply.encode('utf-8')
            conn.send(reply)
        except KeyboardInterrupt:
            conn.close()
            server.close()
            sys.exit()

    conn.close()
    server.close()
