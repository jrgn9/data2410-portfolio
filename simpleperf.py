# simpleperf is a program based on the iPerf tool for measuring network throughput.
# This program is a simplified network throughput measurement tool. 
# simpleperf sends and recieves packet between a client and a server using sockets.
# It runs in two modes: Server mode and client mode.

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

# ERROR HANDLING: FUNCTIONS TO CHECK INPUT VALUES

# Uses ipaddress import to check if the address is a valid ip address
def check_ip(ip_address):
    try:    # This imported function uses ip_address as an argument
        valid = ipaddress.ip_address(ip_address)
    except ValueError:  # Imported function gives a value error if the ip address is not valid
        print(f'[INVALID IP] The IP address \'{ip_address}\' is not a valid address!')  # Prints error message
        raise argparse.ArgumentError("")    # raises an ArgumentError in argparse
    else:   # If there are no ValueError:
        print(f"[SUCCESS] The IP address {valid} is valid")
        return ip_address

# Checks if a port is between 1024 and 65535
def check_port(port):
    try:        # Tries to cast the port to int
        value = int(port)
    except: # If it can't cast port to int, gives an error
        raise argparse.ArgumentTypeError("[VALUE ERROR] Expected an integer")
    
    else:   # If port can be cast to an int
        if (value >= 1024 and value <= 65535):    # If the port has the valid values
            print("[SUCCESS] port value is valid")
            return value
        else:   # Gives an error if the port is out of range
            print("[VALUE ERROR] Expected port between 1024 and 65535")
            raise argparse.ArgumentError("")

# Check that the argument is an int and a positive number
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

# Checks amount of bytes the user specifies by the -n flag. Strips number from byte type
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


# ARGPARSE - A USER FRIENDLY CLI FOR USER ARGUMENTS

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

""" 
# ERROR HANDLING FOR WRONG FLAG AND MODE COMBINATIONS

########## SERVER MODE OG BIND GIR FLAG COMBO ERROR NÅ!!!!!!!!!!!!!!!!!!!!!!
if args.serverip != '127.0.0.1':
    client_serverip = args.serverip
if args.bind != '127.0.0.1':
    bind = args.bind
if args.time != 25:
    client_time = args.time
if args.parallel != 1:
    parallel = args.parallel

if ((args.client and bind) or (args.server and (client_serverip or client_time or args.interval or parallel or args.num))):
    parser.print_help()
    print("\n *****************************************************")
    print("\n \n [FLAG ERROR] Wrong mode and flag combination! \n \n SEE THE HELP MENU ABOVE FOR FLAGS AND ARGUMENTS")
    sys.exit()

 """

# CREATES RESULTS AND PRINT TABLE - Based on what is sent from the server and client functions
def create_result(mode, addr, start_time, end_time, data):
    ip = addr[0]    # Chooses index 0 and 1 from the address tupple to split ip and port
    port = addr[1]
    total_time = end_time - start_time  # Calculates total time based on start and end time provided by client/server
    
    rate = ((data / total_time) / 1000000 ) * 8 # Calculate rate based on data and time provided. Multiplied by 8 for megabytes

    # If/else if to check if the format chosen is MB, KB or B. Then converts the data from byte to the correct format.
    if args.format == 'MB':
        data = data / 1000000        # divides data with 1000000 and cast to int for value in MB
    elif args.format == 'KB':
        data = data/1000             # divides data with 1000 and cast to int for value in KB
    
    # Table from PrettyTable
    result_table = PrettyTable()    # Creates new table
    # Checks if the mode invoked is from server or client. Different field names for the two modes.
    if mode == 'C':
        result_table.field_names = ["ID", "Interval", "Transfer", "Bandwith"]
    elif mode == 'S':
        result_table.field_names = ["ID", "Interval", "Recieved", "Rate"]
    else:
        print("Error in creating result: Wrong mode")   # Error in the edge case that there is no mode chosen (won't really happen)

    # Adds row with all the data provided, with the right rounding and casting of data
    result_table.add_row([f"{ip}:{port}", f"0.0 - {round(total_time, 1)}", f"{int(data)}{args.format}", f"{round(rate, 2)} Mbps"])
    # LØKKE HER FOR Å FÅ UT FLERE RESULTATER
    result_table.add_row(["----------------","---------","--------","----------"])  # Adds a line to split out the summary from all the results
    # OBS!!! MÅ HA EN SUMMARY PRINT TIL SLUTT - SE OPPGAVE
    result_table.add_row(["A summary", "will be", "printed", "here soon"])
    print(result_table) # Prints the table
    print("")


# FUNCTION FOR HANDLING THE SERVER MODE
def server_mode():
    port = int(args.port)    # port from input
    server_ip = args.bind   #   server_ip from input
    addr = (server_ip, port) #    server_ip and port called addr to simply

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Defines socket with family and type
    sock.bind(addr)     # Binds address to the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Sock option that allows for reuse of address

    # Function for handling each client connecting to the server
    def handle_client(conn, addr):
        print(f"A simpleperf client with <{addr[0]}:{addr[1]}> is connected with <{server_ip}:{port}> \n")
        start_time = time.time()    # The start time for the connection
        end_time = 0 # Declare end_time, to be used for later
        data = b''   # Sets data to be an empty byte object
        
        # Recieves byte in packets of 1000 bytes, then add them to data for total amount of bytes
        while True:
            #OBS: HAR FJERNET TRY/EXCEPT/ELSE HER!!!
            part = conn.recv(1000)  # Recieves a request for 1000 bytes
            data += part    # If there still is more parts, add them to data

            #bye_msg = re.search(b'BYE', data)    # Search with regex if the data contains BYE
            #if bye_msg is not None:    # if there is a BYE message. bye_msg is None if it was not found in data
            if b'BYE' in data:  # If there is BYE in bytes in the data
                end_time = time.time()  # Sets end time
                conn.sendall(b'ACK:BYE')   # Sends acknowledge to server that there is a bye message
                conn.close()    # Closes the connection
                data = len(data) - 3    # Sets data to be the length of all the bytes. Subtract 3 for BYE message
                break   # Breaks the while loop
        create_result('S', addr, start_time, end_time, data)  # Calls the function to create results and send all the data

    # Function for starting the server
    def start_server():
        sock.listen()   # Socket listens for connections
        print(f"{line} \t A simpleperf server is listening on port {port} {line}")

        while True:    # Runs as long as there is a connection
            try:
                conn, addr = sock.accept()  # Accepts connection for the incoming address
            except: # If the server can't connect with the server. Prints error and close connection
                print("[ERROR] Could not connect")
                conn.close()
                break
            else:   # If there are no errors
                thread = threading.Thread(target=handle_client, args=(conn, addr))  # Creates new thread where target is the client function and sends the connection and address
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} \n") # Prints how many active connections there are. -1 because listen always run as a thread.

    start_server()  # Starts the server when invoked


# FUNCTION FOR HANDLING THE CLIENT MODE
def client_mode():
    server_ip = args.serverip   # server_ip from input
    server_port= int(args.port)       # port from input
    server_addr = (server_ip, server_port)    # server_ip and port called addr to simply

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Defines socket with family and type

    packet = b"0" * 1000    # Packet to be sent defined as 1000 bytes
    send_time = int(args.time)            # Defined time as the time from user input

    # Function for starting the client
    def start_client():
        print(f"{line} A simpleperf client connecting to server {server_ip}, port {server_port} {line}")
        try:    # Tries to connect to the server address
            sock.connect(server_addr)
        except: # Prints error if it can't connect to server
            print("[ERROR] Could not connect, please try again")
        else:   # If there are no errors
            # Declares the client address
            client_ip = sock.getsockname()[0]
            client_port = sock.getsockname()[1]
            client_addr = (client_ip, client_port)

            print(f"Client connected with {server_ip} port {server_port} \n")
            start_time = time.time()    # Sets start time
            bytes = args.num    # Bytes are the number set in CLI
            if bytes != None:    # If there are defined number of bytes to be sent
                total_bytes = bytes # Sets how many bytes from start
                while bytes:    # As long as there are more bytes
                    if bytes < 1000:    # If there is less than 1000 bytes
                        sock.send(b"0" * bytes) # Sends bytes as 0 as many times as there are bytes left
                        break   # Ends the loop
                    sock.send(packet)   # If there are > 1000 bytes, keep sending packets of 1000 bytes.
                    bytes -= 1000   # Subtract 1000 bytes from the amount given by user
                end_time = time.time()  # Sets end time when the loop is done
                
            else:           # If there are not defined number, but time instead
                total_bytes = 0 # Declares total bytes to be used for later
                end_time = start_time + send_time   # Defines end time as the start + time chosen by user
                while time.time() < end_time:   # As long as the current time is less then the end time
                    sock.send(packet)   # Sends packets of 1000 bytes
                    total_bytes += 1000 # Adds 1000 bytes to the total amount of bytes sent
            sock.sendall(b'BYE')    # Sends BYE message to server when the time is up
            server_msg = sock.recv(1024)    # Recives message back from server
            create_result('C', client_addr, start_time, end_time, total_bytes)  # Calls the create result function with the data
            if server_msg == b'ACK:BYE':    # If the server has acknowledged the BYE message
                print("[SUCCESS] Server acknowledged BYE message \n")   # Print message to show that it succeeded
                #create_result('C', client_addr, start_time, end_time, total_bytes)
            else:
                print("[ERROR] Unexpected response from server")    # Prints error if there is no response/wrong response from server
            sock.close()    # Closes the connection when done

    start_client()  # Starts the client when invoked


# INVOKING CLIENT OR SERVER MODE
#Gives error if both or none of the mode flags are chosen
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