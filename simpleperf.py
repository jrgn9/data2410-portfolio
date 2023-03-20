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
    type=bool, 
    help='enable the server mode. Choosing server or client mode are required.')
parser.add_argument(
    '-b', '--bind',
    type=int,
    default='127.0.0.1',
    help='allows to select the ip address of the servers interface where the client should connect. It must be in the dotted decimal notation format, e.g. 10.0.0.2')

# CLIENT ARGUMENTS:
parser.add_argument(
    '-c', '--client', 
    type=bool,
    help='enable the client mode. Choosing server or client mode are required.')
parser.add_argument('-I', '--serverip')
parser.add_argument('-t', '--time')
parser.add_argument('-i', '--interval')
parser.add_argument('-P', '--parallel')
parser.add_argument('-n', '--num')

# COMMON ARGUMENTS:
parser.add_argument(
    '-p', '--port',
    type=int,
    default=8088,
    help='allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088')
parser.add_argument(
    '-f', '--format',
    type=str,
    choices=['B', 'KB', 'MB'],
    default='MB',
    help='allows you to choose the format of the summary of results - it should be either in B, KB or MB, default=MB)')

# FUNCTIONS TO CHECK INPUT VALUES