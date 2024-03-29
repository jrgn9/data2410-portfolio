'''
simpleperf is a program based on the iPerf tool for measuring network throughput.
This program is a simplified network throughput measurement tool. 
simpleperf sends and recieves packet between a client and a server using sockets.
It runs in two modes: Server mode and client mode. It has different flags for extra functionality.
'''

# Different module imports used in this program
import argparse # argparse is used for a user friendly command-line interface. Here the user can give arguments when running the program
import ipaddress    # can be used to check if an ip address is valid. Returns ValueError if not valid
import re   # Regex functions
import sys  # Functions that interact with the interpreter. Like sys.exit()
import socket   # Functions for socket operations
import threading    # Functions for server threading
import time # Various time functions
from prettytable import PrettyTable # Table formating library. Must be installed with pip: python -m pip install -U prettytable

# Used to formating, creating lines for print messages
line = "\n" + "-" * 65 + "\n"

'''
Error handling for ip addresses. Uses the Uses ipaddress import to check if the address is a valid ip address.
The imported function gives a ValueError if the provided ip address is not a valid IPv4 or IPv6 address.
Returns the ip address if it passes the check
'''
def check_ip(ip_address):
    try:    # This imported function uses ip_address as an argument
        valid = ipaddress.ip_address(ip_address)
    except ValueError:  # Imported function gives a value error if the ip address is not valid
        print(f'[INVALID IP] The IP address \'{ip_address}\' is not a valid address!')  # Prints error message
        raise argparse.ArgumentError("")    # raises an ArgumentError in argparse
    else:   # If there are no ValueError:
        return ip_address

'''
Error handling for port. Checks if the port can be casted to an integer. Then it checks if the value is
between 1024 and 65535 which is the permitted range. Returns the port if it passes the check.
'''
def check_port(port):
    try:        # Tries to cast the port to int
        value = int(port)
    except: # If it can't cast port to int, gives an error
        raise argparse.ArgumentTypeError("[VALUE ERROR] Expected an integer")
    
    else:   # If port can be cast to an int
        if (value >= 1024 and value <= 65535):    # If the port has the valid values
            return value
        else:   # Gives an error if the port is out of range
            print("[VALUE ERROR] Expected port between 1024 and 65535")
            raise argparse.ArgumentError("")

'''
Checks that the argument can be casted to an integer and that the value is positive.
This function is used by time and interval, which requires a positive integer.
Returns the number if it is a positive integer.
'''
def check_positive(num):
    try:
        value = int(num)    # Tries to cast the number to an int
    except: # If it can't cast port to int, gives an error
        raise argparse.ArgumentTypeError("[VALUE ERROR] Expected an integer")
    else:   # If port can be cast to an int
        if (value >= 0):
            return num
        else:   # Gives an error if the number is negative
            print("[VALUE ERROR] Expected a positive integer")
            raise argparse.ArgumentError("")

'''
Error handling for the --num flag. The flag is taking both a number and format as an argument.
First this function tries to split number and letters with regex, then checks if the number is
an integer. It checks if the format given are B, KB or MB and if not gives an error message to the user.
Returns the value from the user as bytes.
'''
def check_num(bytes):
    try:
        byte_type = re.sub('[0-9]','', bytes)    # Strips the input for numbers
        upper_type = byte_type.upper()   # Converts the string to upper case
        amount = re.sub('[A-Za-z]','', bytes)   # Strips the input for lower and upper case letters
        byte_amount = int(amount)   # Tries to cast the stripped input to int
    except ValueError:  # If amount can't be cast to int after being stripped
        print("[VALUE ERROR] Error in number of bytes. it should be either in B, KB or MB. e.g. 1MB")
        raise argparse.ArgumentError("")
    else:   # If no errors: Checks if the value is in bytes, kb or mb and then returns the amount in bytes
        if (upper_type == 'B'):
            return byte_amount
        elif (upper_type == 'KB'):
            return byte_amount * 1000
        elif (upper_type == 'MB'):
            return byte_amount * 1000000
        else:   # If the byte type was not converted to B, KB or MB
            print("[VALUE ERROR] Error in number of bytes. it should be either in B, KB or MB. e.g. 1MB")
            raise argparse.ArgumentError("")

'''
ARGPARSE:
An user friendly CLI for user arguments. It is a command-line parsing library that gives instruction to the user,
lets the user choose different arguments and makes it easy to create limitations.
Used here to create a help menu, set flags, instructions, arguments and restrictions. Returns arguments to be used in the code.
'''
# argparse parser object with a description of what this program do
parser = argparse.ArgumentParser(
    prog="simpleperf",
    description="A simple program based on the iPerf tool for measuring network throughput, with a server and a client mode. simpleperf sends and recieves packet between a client and a server using sockets", 
    epilog="END OF HELP")

# ADDS ARGUMENTS TO THE ARGPARSER

# SERVER ARGUMENTS: Own argument group to show arguments for server only
serverargs = parser.add_argument_group("SERVER ARGUMENTS:", "Arguments for server mode only")
serverargs.add_argument('-s', '--server', action='store_true', help='enable the server mode. Choosing server or client mode are required.')
serverargs.add_argument('-b', '--bind', type=check_ip, default='127.0.0.1',
    help='allows to select the ip address of the servers interface where the client should connect. It must be in the dotted decimal notation format, e.g. 10.0.0.2 - Default: 127.0.0.1')

# CLIENT ARGUMENTS: Own argument group to show arguments for client only
clientargs = parser.add_argument_group("CLIENT ARGUMENTS:", "Arguments for client mode only")
clientargs.add_argument('-c', '--client', action='store_true', help='enable the client mode. Choosing server or client mode are required.')
clientargs.add_argument('-I', '--serverip', type=check_ip, default='127.0.0.1', 
    help='allows to select the ip address of the server. It must be in the dotted decimal notation format, e.g. 10.0.0.2 - Default: 127.0.0.1')
clientargs.add_argument('-t', '--time', type=check_positive, default=25, help='the total duration in seconds for which data should be generated, also sent to the server. Must be > 0. Default: 25 sec')
clientargs.add_argument('-i', '--interval', type=check_positive, help='print statistics per x seconds')
clientargs.add_argument('-P', '--parallel', type=int, choices=range(1,6), default=1, help='creates parallel connections to connect to the server and send data - min value: 1, max value: 5 - default:1')
clientargs.add_argument('-n', '--num', type=check_num, help='transfer number of bytes specified by -n flag, it should be either in B, KB or MB. e.g. 1MB')

# COMMON ARGUMENTS: Own argument group to show arguments for both modes
commonargs = parser.add_argument_group("COMMON ARGUMENTS:", "Arguments for both server and client mode")
commonargs.add_argument('-p', '--port', type=check_port, default=8088, 
    help='allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088')
commonargs.add_argument('-f', '--format', type=str, choices=['B', 'KB', 'MB'], default='MB', help='allows you to choose the format of the summary of results - it should be either in B, KB or MB, default=MB)') 

# Variable for the user argument inputs
args = parser.parse_args()


'''
CREATE RESULTS:
Function for creating print message with results. Uses the PrettyTable library to format the results in tables.
The function takes server/client mode, ip and port, start time, interval start (if interval is set), elapsed time, data and 
a boolean for if there are interval set or not. If there is not an interval set, it will print the summary.
First finds the rate by using data and elapsed time. Checks which format is set. Then creates a PrettyTable, checks which mode is
set and creates a header row based on that. Checks if there is an interval set, and adds results to the row accordingly. 
'''
def create_result(mode, addr, start_time, interval_start, elapsed_time, data, interval=False):
    ip = addr[0]    # Chooses index 0 and 1 from the address tupple to split ip and port
    port = addr[1]
    relative_interval_start = interval_start - start_time   # Sets the start for every interval

    rate = (data / elapsed_time) * 8 / 1000000 # Calculate rate based on data and time provided. Multiply by 8 to convert to bits pr sec

    # If/else if to check if the format chosen is MB, KB or B. Then converts the data from byte to the correct format.
    if args.format == 'MB':
        data = data // 1000000        # divides data with 1000000 and cast to int for value in MB
    elif args.format == 'KB':
        data = data // 1000             # divides data with 1000 and cast to int for value in KB
    
    # Table from PrettyTable
    result_table = PrettyTable()    # Creates new table
    # Checks if the mode invoked is from server or client. Different field names for the two modes.
    if mode == 'C':
        result_table.field_names = ["ID", "Interval", "Transfer", "Bandwith"]
    elif mode == 'S':
        result_table.field_names = ["ID", "Interval", "Recieved", "Rate"]
    else:
        print("Error in creating result: Wrong mode")   # Error in the edge case that there is no mode chosen (won't really happen)

    # String for interval time printing dependent on if interval=True/False
    if interval:
        interval_str = f"{round(relative_interval_start, 1)} - {round(relative_interval_start + elapsed_time, 1)}"  # Prints interval from rel. start to rel. start + elapsed time
    else:
        interval_str = f"0.0 - {round(elapsed_time, 1)}"    # If there is no interval (just summary), prints 0.0 to elapsed time

    # Adds row with all the data provided, with the right rounding and casting of data
    result_table.add_row([f"{ip}:{port}", interval_str, f"{data}{args.format}", "%.2f Mbps" % rate])
    print(result_table)
    print("")

'''
HANDLE CLIENTS:
A function for handling each client connecting to the server. Function called from the start_server function.
Takes socket connection, client address, server ip and server port as arguments.
In an infinite while loop it tries to receive data from client. Keeps receiving data and adds them in a variable.
Checks if there are no data or a BYE message and closes connection. Then sends all the data to create_results.
'''
def handle_client(conn, addr, server_ip, port):
    print(f"A simpleperf client with <{addr[0]}:{addr[1]}> is connected with <{server_ip}:{port}> \n")
    start_time = time.time()    # The start time for the connection
    end_time = 0 # Declare end_time, to be used for later
    recv_bytes = 0  # Declare recieved bytes

    while True: # Infinite loop
        try:    # Tries to recive data from client
            data = conn.recv(1000)  # Sets data as recieved data from client
        except:
            print("[ERROR] Could not receive data from client. Connection closed")
            conn.close()
        else:   # If there are no errors
            if not data:    # Stops if there are no more data
                break
            if b'BYE' in data:  # If there is a BYE message in data
                recv_bytes += len(data) - len(b'BYE')  # Subtract the length of the 'BYE' message
                conn.send(b'ACK:BYE')   # Sends ACK BYE back to client
                break
            else:   # If there are data and no BYE message
                recv_bytes += len(data) # Adds the length of the recieved bytes to the variable

    end_time = time.time()  # Sets end time
    elapsed_time = end_time - start_time    # Sets elapsed time to send to results
    create_result('S', addr, start_time, end_time, elapsed_time, recv_bytes, False)  # Calls the function to create results and send all the data. False for interval
    conn.close()

'''
START SERVER:
A function for starting the server. Listens for connections. If there are a connection, it starts a new thread and sends it to
the handle_client function. Checks if there are a connection and closes if there are none.
'''
def start_server(sock, server_ip, port):
    sock.listen()   # Socket listens for connections
    print(f"{line} \t A simpleperf server is listening on port {port} {line}")

    sock.settimeout(900)    # Set a timeout of 15 minutes for the server socket

    while True:    # Runs as long as there is a connection
        conn = None  # Initialize conn variable
        try:
            conn, addr = sock.accept()  # Accepts connection for the incoming address
        except socket.timeout:
            # If no clients connect in 15 minutes
            print("[CONNECTION TIMEOUT] Timeout due to inactivity. Closing connections...")
            if conn:
                conn.close()
            sys.exit(0)
        except KeyboardInterrupt:
            # If the user hits ctrl+c, close the server socket and any open connections
            print("[CLOSING CONNECTIONS] Goodbye!")
            if conn:
                conn.close()
            sys.exit(0)
        except: # If the server can't connect with the server. Prints error and close connection
            print("[ERROR] Could not connect")
            if conn:
                conn.close()
        else:   # If there are no errors
            thread = threading.Thread(target=handle_client, args=(conn, addr, server_ip, port))  # Creates new thread where target is the client function and sends the connection and address
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} \n") # Prints how many active connections there are. -1 because listen always run as a thread.

'''
SERVER MODE:
A function for handling the server mode. If the mode is invoked it gets the address from the user, creates a socket 
and sends it to the start_server function.
'''
def server_mode():
    port = int(args.port)    # port from input
    server_ip = args.bind   #   server_ip from input
    addr = (server_ip, port) #    server_ip and port called addr to simply

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Defines socket with family and type
    sock.bind(addr)     # Binds address to the socket

    start_server(sock, server_ip, port)  # Starts the server when invoked

'''
START CLIENT:
A function for starting (and running) the client. Takes socket and address as arguments.
Tries to connect to the server. Then checks if there is set an interval and handles that accordingly.
Checks if there is selected number of bytes or time, then runs a loop handling that.
'''
def start_client(sock, server_ip, port):
    server_addr = (server_ip, port)
    send_time = int(args.time)            # Defined time as the time from user input
    packet = b"0" * 1000    # Packet to be sent defined as 1000 bytes

    print(f"{line} A simpleperf client connecting to server {server_ip}, port {port} {line}")
    
    try:    # Tries to connect to the server address
        sock.connect(server_addr)
    except: # Prints error if it can't connect to server
        print("[ERROR] Could not connect, please try again")
    else:   # If there are no errors
        # Declares the client address
        client_ip = sock.getsockname()[0]
        client_port = sock.getsockname()[1]
        client_addr = (client_ip, client_port)

        print(f"Client connected with {server_ip} port {port} \n")
        
        start_time = time.time()    # Sets start time                
        bytes = args.num    # Bytes are the number set in CLI
        total_bytes = 0 # declares total bytes

        # Declares variables for interval flag:
        if args.interval is not None:   # Checks if a interval is set
            interval = int(args.interval)
        else:
            interval = None
        interval_start = start_time
        interval_bytes = 0

        '''
        NUMBER OF BYTES: 
        If there are defined number of bytes with the -n flag
        '''  
        # IF THERE ARE DEFINED BYTES WITH --NUM
        if bytes != None:
            total_bytes = bytes # Sets how many bytes from start
            while bytes > 0:    # As long as there are more bytes

                if bytes < 1000:    # If there is less than 1000 bytes
                    sock.send(b"0" * bytes) # Sends bytes as 0 as many times as there are bytes left
                    interval_bytes += bytes # Adds to interval_bytes
                    bytes = 0   # No more bytes
                sock.send(packet)   # If there are > 1000 bytes, keep sending packets of 1000 bytes.
                interval_bytes += len(packet)   # Adds bytes to interval bytes
                bytes -= 1000   # Subtract 1000 bytes from the amount given by user

                '''
                INTERVAL FLAG:
                If there is set an interval for printing results, it will keep sending data to the create_result function
                '''
                current_time = time.time()
                if interval and current_time - interval_start >= interval:  # If there is set an interval and we hit the interval
                    elapsed_time = current_time - interval_start    # Elapsed time is the current time subtracted by when the interval started
                    create_result('C', client_addr, start_time, interval_start, elapsed_time, interval_bytes, True)   # Creates result with the interval given
                    # "Reset" start time and interval bytes
                    interval_start = current_time
                    interval_bytes = 0
            end_time = time.time()  # Sets end time when the loop is done
            sock.send(b'BYE')   # Send the BYE message after sending the specified amount of data
        
            '''
        TIME MODE: 
        If bytes (num) are not defined, it will either be default (25 sec) or defined by the time flag.
        A while loop that runs as long as the current time is less then the defined end time.
        '''
        else:
            end_time = start_time + send_time   # Defines end time as the start + time chosen by user
            while time.time() < end_time:   # As long as the current time is less then the end time
                remaining_time = end_time - time.time() # Defines how long is remaining
                sock.send(packet)   # Sends packets of 1000 bytes
                total_bytes += len(packet) # Adds length of packet to the total amount of bytes sent
                interval_bytes += len(packet)   # Adds bytes to the interval_bytes

                '''
                INTERVAL FLAG:
                If there is set an interval for printing results, it will keep sending data to the create_result function
                '''
                current_time = time.time()
                if interval and current_time - interval_start >= interval:  # If there is set an interval and we hit the interval
                    elapsed_time = current_time - interval_start    # Elapsed time is the current time subtracted by when the interval started
                    create_result('C', client_addr, start_time, interval_start, elapsed_time, interval_bytes, True)   # Creates result with the interval given
                    # "Reset" start time and interval bytes
                    interval_start = current_time
                    interval_bytes = 0
        
        ''' 
        After the num or time loop are finished, the client sends BYE, sends all the data to the create_result function,
        then checks for acknowledgement from the server 
        '''
        sock.send(b'BYE')   # Sends BYE message
        total_elapsed_time = end_time - start_time
        create_result('C', client_addr, start_time, interval_start, total_elapsed_time, total_bytes, False)  # Calls the create result function with the data and no interval (for summary)
        server_msg = sock.recv(1024)    # Recives message back from server
        if server_msg == b'ACK:BYE':    # If the server has acknowledged the BYE message
            print("[SUCCESS] Server acknowledged BYE message \n")   # Print message to show that it succeeded
        else:
            print("[ERROR] Unexpected response from server")    # Prints error if there is no response/wrong response from server.
        sock.close()    # Closes the connection when done

'''
CLIENT MODE:
A function for handling the client mode. If the mode is invoked it gets the address from the user. Checks if there is set a parallel flag,
then starts a new thread for each client set as parallel. Creates a socket and sends the socket and address to the start_client function. 
'''
def client_mode():
    server_ip = args.serverip   # server_ip from input
    server_port= int(args.port)       # port from input

    # For loop that create client threads for each parallel flag set
    for clients in range(0, int(args.parallel)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Defines socket with family and type
        thread = threading.Thread(target=start_client, args=(sock, server_ip, server_port))  # Starts the client when invoked
        thread.start()

'''
INVOKING CLIENT OR SERVER MODE:
Checks if the user has chosen server mode or client mode. Then calls upon their function respectively.
Gives error message if both or none of the mode flags are chosen.
'''
if ((not args.server and not args.client) or (args.server and args.client)):
    parser.print_help() # If not server/client or both are invoked it prints the help screen, then an error message, then exits
    print(line)
    print("[ERROR] you must run either in server or client mode \n \nSEE THE HELP MENU ABOVE FOR FLAGS AND ARGUMENTS \n")
    sys.exit()
elif args.server:   # If server flag is chosen
    print("[SERVER MODE] Starting...")
    server_mode()   # Starts the server mode
elif args.client:   # If client flag is chosen
    print("[CLIENT MODE] Starting...")
    client_mode()   # Starts the client mode
    