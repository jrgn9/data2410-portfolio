# simpleperf is a program based on the iPerf tool for measuring network throughput.
# This program is a simplified network throughput measurement tool. 
# simpleperf sends and recieves packets between a client and a server using sockets.
# It runs in two modes: Server mode and client mode.

# Different function imports used in this program
import argparse
import sys
import ipaddress
import socket
import threading
import time

# argparse is used for a user friendly command-line interface. Here the user can give arguments when running the program

# argparse parser object with a description of what this program do
parser = argparse.ArgumentParser(
    prog="simpleperf",
    description="A simple program based on the iPerf tool for measuring network throughput, with a server and a client mode. simpleperf sends and recieves packets between a client and a server using sockets", 
    epilog="end of help")

# SERVER ARGUMENTS:
parser.add_argument(
    '-s', '--server',
    type=check_mode, 
    help='enable the server mode. Choosing server or client mode are required.')
parser.add_argument(
    '-b', '--bind',
    type=check_ip,
    default='127.0.0.1',
    help='allows to select the ip address of the servers interface where the client should connect. It must be in the dotted decimal notation format, e.g. 10.0.0.2 - Default: 127.0.0.1')

# CLIENT ARGUMENTS:
parser.add_argument(
    '-c', '--client', 
    type=check_mode,
    help='enable the client mode. Choosing server or client mode are required.')
parser.add_argument(
    '-I', '--serverip',
    type=check_ip,
    default='127.0.0.1',
    help='allows to select the ip address of the server. It must be in the dotted decimal notation format, e.g. 10.0.0.2 - Default: 127.0.0.1')
parser.add_argument(
    '-t', '--time',
    type=check_positive,
    default=25,
    help='the total duration in seconds for which data should be generated, also sent to the server. Must be > 0. Default: 25 sec'
    )
parser.add_argument(
    '-i', '--interval',
    type=check_positive,
    help='print statistics per x seconds')
parser.add_argument(
    '-P', '--parallel',
    choices=range(1,5),
    default=1,
    help='creates parallel connections to connect to the server and send data - min value: 1, max value: 5 - default:1')
parser.add_argument(
    '-n', '--num',
    type=check_num,
    help='transfer number of bytes specified by -n flag, it should be either in B, KB or MB. e.g. 1MB')

# COMMON ARGUMENTS:
parser.add_argument(
    '-p', '--port',
    type=check_port,
    default=8088,
    help='allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088')
parser.add_argument(
    '-f', '--format',
    type=str,
    choices=['B', 'KB', 'MB'],
    default='MB',
    help='allows you to choose the format of the summary of results - it should be either in B, KB or MB, default=MB)')

# ERROR HANDLING: FUNCTIONS TO CHECK INPUT VALUES

def check_mode(mode):
    # if -s - return server
    # if -c - return client
    # else - error message
    pass

def check_ip(ip_address):
    # Uses ipaddress import to check if the address is a valid ip address
    
    try:
        # This imported function uses ip_address as an argument
        valid = ipaddress.ip_address(ip_address)

    # Imported function gives a value error if the ip address is not valid
    except ValueError:
        print(f"The IP address {valid} is not valid")
        # RETURN SOMETHING?
    
    # If there are no ValueError:
    else:
        print(f"The IP address {valid} is valid")
        # RETURN SOMETHING?

def check_port(port):
    # check for int, then check for value >= 1024, <= 65535 

    try:
        value = int(port)
    except:
        raise argparse.ArgumentTypeError("[VALUE ERROR] Expected an integer")
    else:
        if (value >= 1024 & value <= 65535):
            print("correct port value")
            #RETURN SOMETHING?
        else:
            raise argparse.ArgumentError(value, "[VALUE ERROR] Expected port between 1024 and 65535")
            # sys.exit() ???


def check_positive(num):
    # Check that it is a int and a positive number 
    pass

def check_num(bytes):
    # split, then check for int and B, KB, MB
    pass