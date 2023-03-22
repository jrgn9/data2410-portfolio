# simpleperf is a program based on the iPerf tool for measuring network throughput.
# This program is a simplified network throughput measurement tool. 
# simpleperf sends and recieves packets between a client and a server using sockets.
# It runs in two modes: Server mode and client mode.

# Different function imports used in this program
import argparse # argparse is used for a user friendly command-line interface. Here the user can give arguments when running the program
import ipaddress    # can be used to check if an ip address is valid. Returns ValueError if not valid
import re   # Regex functions
import sys
import socket
import threading
import time


# ERROR HANDLING: FUNCTIONS TO CHECK INPUT VALUES

# Uses ipaddress import to check if the address is a valid ip address
def check_ip(ip_address):
    try:    # This imported function uses ip_address as an argument
        valid = ipaddress.ip_address(ip_address)
    except ValueError:  # Imported function gives a value error if the ip address is not valid
        print(f'[INVALID IP] The IP address \'{ip_address}\' is not a valid address!')  # Prints error message
        raise argparse.ArgumentError("")    # raises an ArgumentError in argparse
    else:   # If there are no ValueError:
        if (ip_address != '127.0.0.1'):  # To avoid getting message for valid IP for when no IP is given (default IP)
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
            print("[SUCCESS] Port value is valid")
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

def check_num(bytes):   # transfer number of bytes specified by -n flag, it should be either in B, KB or MB. e.g. 1MB
    byte_type = re.sub(r"[^a-zA-Z]+", "", bytes)    # Strips the input for anything other than a-z and A-Z
    byte_type.upper()   # Converts the string to upper case
    byte_amount = re.sub(r"[^0-9", "", bytes)   # Strips the input for anything other than numbers

    print("Byte type:" + byte_type)
    print("Byte amount:" + byte_amount)
    
    # Checks if the value is in bytes, kb or mb and then returns the amount in bytes
    if (byte_type == 'B'):
        return byte_amount
    elif (byte_type == 'KB'):
        return byte_amount * 1000
    elif (byte_type == 'MB'):
        return byte_amount * 1000000
    else:
        print("Something went wrong with check_num")
        raise argparse.ArgumentError(value, "[VALUE ERROR] Error in number of bytes. it should be either in B, KB or MB. e.g. 1MB")

# ARGPARSE - A USER FRIENDLY CLI FOR USER ARGUMENTS

# argparse parser object with a description of what this program do
parser = argparse.ArgumentParser(
    prog="simpleperf",
    description="A simple program based on the iPerf tool for measuring network throughput, with a server and a client mode. simpleperf sends and recieves packets between a client and a server using sockets", 
    epilog="end of help")

# ADDS ARGUMENTS TO THE ARGPARSER

# SERVER ARGUMENTS:
parser.add_argument('-s', '--server', action='store_true', help='enable the server mode. Choosing server or client mode are required.')
parser.add_argument('-b', '--bind', type=check_ip, default='127.0.0.1',
    help='allows to select the ip address of the servers interface where the client should connect. It must be in the dotted decimal notation format, e.g. 10.0.0.2 - Default: 127.0.0.1')

# CLIENT ARGUMENTS:
parser.add_argument('-c', '--client', action='store_true', help='enable the client mode. Choosing server or client mode are required.')
parser.add_argument('-I', '--serverip', type=check_ip, default='127.0.0.1', 
    help='allows to select the ip address of the server. It must be in the dotted decimal notation format, e.g. 10.0.0.2 - Default: 127.0.0.1')
parser.add_argument('-t', '--time', type=check_positive, default=25, help='the total duration in seconds for which data should be generated, also sent to the server. Must be > 0. Default: 25 sec')
parser.add_argument('-i', '--interval', type=check_positive, help='print statistics per x seconds')
parser.add_argument('-P', '--parallel', type=int, choices=range(1,6), default=1, help='creates parallel connections to connect to the server and send data - min value: 1, max value: 5 - default:1')
#parser.add_argument('-n', '--num', type=check_num, help='transfer number of bytes specified by -n flag, it should be either in B, KB or MB. e.g. 1MB')

# COMMON ARGUMENTS:
parser.add_argument('-p', '--port', type=check_port, default=8088, 
    help='allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088')
parser.add_argument('-f', '--format', type=str, choices=['B', 'KB', 'MB'], default='MB', help='allows you to choose the format of the summary of results - it should be either in B, KB or MB, default=MB)') 

# Variable for the user argument inputs
args = parser.parse_args()

# parser.print_help()

if ((not args.server and not args.client) or (args.server and args.client)):
    print("error, u must choose server OR client mode. Not both. Or none.")
elif args.server:
    print("server kjører bitch")
    # Brukes til å starte server() funksjon
elif args.client:
    print("klient kjører bitch")
    # Brukes til å starte client() funksjon





#### OBS!!! FEILHÅNDTER client/server opp mot -I og -b flags

# Prøv å lage en feilhåndtering for flags som ikke hører sammen her

# parser.print_help()


'''

def client_mode():
    # Setter HOST, PORT og FILE til å være user argument 0,1 og 2
    HOST = sys.argv[1]
    PORT = int(sys.argv[2]) # Burde kanskje hatt error handling for PORT, men lot være i denne oppgaven.
    FILE = sys.argv[3]
    ADDR = (HOST, PORT)
    FORMAT = "utf-8"
    print(ADDR, FILE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Definerer socket med socket familie og type


    #print("[ERROR] Could not connect")

    def recieve():
        try:
            sock.connect(ADDR)
            request = f"GET /{FILE} HTTP/1.1"
            request = request.encode(FORMAT)
            sock.send(request)
            print(sock.recv(99999).decode(FORMAT))
        except:
            pass

    recieve()

def server_mode():
    # Final/static variabler
    PORT = 9999 # Setter port
    HOST = socket.gethostbyname(socket.gethostbyname(socket.gethostname()))   # Finner host ip automatisk
    ADDR = (HOST, PORT) # Kaller host og port for ADDR (for å forenkle videre)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Definerer socket med socket familie og type
    sock.bind(ADDR) # binder adressen til socketen
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Hva gjør denne???

    def handle_client():
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") # prints how many connections that are active in this process
        pass

    #Funksjon for å starte serveren
    def start():
        sock.listen()   # Socket lytter etter connections
        print(f"[LISTENING] Server listening on {ADDR} \n") # Melding som viser host adresse som lyttes til

        connected = True
        while connected: # Kjører så lenge det er en connection
            conn, addr = sock.accept()    # Aksepter connection på adressen som kommer inn
            request = conn.recv(1024).decode()  # Tar imot request på 1024 bytes
            print(f"[REQUEST] {request}")   # Printer ut requesten til serveren

            # FEILHÅNDTERING:
            try:    # Prøver å åpne html-filen
                # Åpne html fil
                file = open("index.html", "r")  # HVA GJØR r???

            except FileNotFoundError: # Hvis filen ikke lar seg åpnes/ikke finnes
                # Sender feilmelding, lager 404 responsmelding og lukker connection
                fail_msg = "[ERROR] 404 Not Found"
                fail_msg = fail_msg.encode()
                conn.send(fail_msg)
                print("[CONNECTION CLOSED] Error 404 Not Found")
                response = "HTTP/1.1 404 Not Found\n"
                response = response.encode()
                conn.close()
                connected = False

            else:   # Hvis filen kan åpnes
                #leser html fil
                content = file.read()
                file.close()

                # Lager responsmelding
                response = "HTTP/1.1 200 OK\n"
                response += "Content-Type: text/html\n"
                response += "Content-Length: {}\n".format(len(content))
                response += "\n"
                response += content
                response = response.encode()

                #Sender responsmelding og lukker connection
                conn.send(response)
                print(f"[RESPONSE SENT] {response}")
                print("[CONNECTION CLOSED]")
                conn.close()
                connected = False

    # Starter serveren
    print("[STARTING] Server is starting")  # Melding om at serveren starter
    start() # Kaller på funksjonen til å starte serveren

'''