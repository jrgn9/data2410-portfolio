# DATA2410 - Portfolio 1

This is a repository for the coding part of portfolio 1 in the DATA2400 subject.

## iPerf
iPerf is a tool for measuring network throughput. In this project, you’ll design and implement simpleperf - your own simplified version of iperf using sockets. The simpleperf tool you write will run on a virtual network managed by mininet inside a virtual machine. You’ll use it to measure the performance of a network.

## Implement simpleperf
You’ll implement a simple network throughput measurement tool - simpleperf. Your tool is supposed to send and receive packets between a client and a server using sockets. Your simpleperf tool MUST run in two modes: 

1) Server mode,
and 
2) Client mode

### Server mode
When you run in server mode, simpleperf will receive TCP packets and track how much data was received during from the connected clients; it will calculate and display the bandwidth based on how much data was received and how much time elapsed during the connection. A server should read data in chunks of 1000 bytes. For the sake of simplcity, assume 1 KB = 1000 Bytes, and 1 MB = 1000KB.


To run simpleperf in server mode with the default options, it should be invoked as follows:

python3 simpleperf -s

* -s indicates simpleperf is running in a server mode: it should receive data and track the total number of bytes

The server should print:
```
---------------------------------------------
A simpleperf server is listening on port XXXX
--------------------------------------------- 
```

**Table below lists all the available options that you can use to invoke the server:**

| **flag** | **long flag** | **input**   | **type**  | **description**                                                                                                                                                                                       |
|:--------:|:-------------:|:-----------:|:---------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| -s       | --server      | X           | (boolean) | enable the server mode                                                                                                                                                                                |
| -b       | --bind        | ip adress   | string    | allows to select the ip address of the server’s interface where the client should connect - use a default value if it’s not provided. It must be in the dotted decimal notation format, e.g. 10.0.0.2 |
| -p       | --port        | port number | integer   | allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088                                                         |
| -f       | --format      | MB          | string    | allows you to choose the format of the summary of results - it should be either in B, KB or MB, default=MB)   

Here is an example how one should be able to invoke the server:

    python3 simpleperf -s -b <ip_address> -p <portnumber> -f MB

And the server should print the following and wait for a connection:
```
---------------------------------------------
    A simpleperf server is listening on port XXXX
---------------------------------------------
```

When a client connects, a server should print:
```
---------------------------------------------
    A simpleperf server is listening on port XXXX
---------------------------------------------
```


    A simpleperf client with <IP address: port> is connected with <server IP:port>

At the end of the transfer, simpleperf client will send a “BYE” message to the
server to indicate that the transfer is complete. The server will then send an
acknowledgement (“ACK: BYE”) to the client, print the results in the following
format, and gracefully close the connection.
```
---------------------------------------------
A simpleperf server is listening on port XXXX
---------------------------------------------

A simpleperf client with <IP address: port> is connected with <server IP:port>
```

| ID      | Interval   | Recieved | Rate   |
|---------|------------|----------|--------|
| IP:port | 0.0 - 25.0 | X MB     | Y Mbps |

**There are four columns here:**

1. ID specifies the client_IP:port pair
   
2. Interval: Total duration in seconds
   
3. Transfer: X stands for the total number of bytes received (in Megabytes,
if not specified with -f. Note X should be an integer.

4. Rate: Y stands for the rate at which traffic could be read in megabits per
second (Mbps). and Y should be a float value with two digits after the
decimal point.

| ID            | Interval   | Recieved | Rate      |
|---------------|------------|----------|-----------|
| 10.0.0.1:3354 | 0.0 - 25.0 | 2544 KB  | 0.82 Mbps |

### Client mode

When we invoke simpleperf in a client mode, it must establish a TCP connec-
tion with the simpleperf server and send data in chunks of 1000 bytes (all zeroes
or same values) for t seconds specified with -t or –time flag. Calculate the total
of the number of bytes sent. After the client finishes sending its data, it should
send a finish/bye message and wait for an acknowledgement before exiting the
program. Simpleperf will calculate and display the bandwidth based on how
much data was sent in the elapsed time.

**To operate simpleperf in client mode, it should be invoked as follows:**

    python3 simpleperf -c -I <server_ip> -p <server_port> -t <time>

* -c indicates this is the simpleperf client mode.
  
* -I specifies the server_ip - IP address of the simpleperf server will
receive data from the simpleperf client

* -p specifies the server_port in which the server is listening to receive
data; the port should be in the range [1024, 65535]

* time is the total duration in seconds for which data should be generated
and sent to the server.

```
------------------------------------------------------------------------------------------
A simpleperf client connecting to server <IP>, port XXXX
------------------------------------------------------------------------------------------

Client connected with server_IP port XXXX
```

| ID      | Interval   | Transfer | Bandwith |
|---------|------------|----------|----------|
| IP:port | 0.0 - 25.0 | X MB     | Y Mbps   |

**Table below lists all the available options that you can use to invoke the server:**

| flag | long flag  | input       | type      | description                                                                                                                                                                                                                          |
|------|------------|-------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -c   | --client   | X           | (boolean) | enable the client mode                                                                                                                                                                                                               |
| -I   | --serverip | ip adress   | string    | allows to select the ip address of the server - use a default value if it’s not provided. It must be in the dotted decimal notation format, e.g. 10.0.0.2                                                                            |
| -p   | --port     | port number | integer   | allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088                                                                                        |
| -t   | --time     | seconds     | integer   | the total duration in seconds for which data should be generated, also sent to the server (if it is set with -t flag at the client side) and must be > 0. NOTE: If you do not use -t flag, your experiment should run for 25 seconds |
| -f   | --format   | MB          | string    | allows you to choose the format of the summary of results - it should be either in B, KB or MB, default=MB)                                                                                                                          |
| -i   | --interval | z           | integer   | print statistics per z second                                                                                                                                                                                                        |
| -P   | --parallel | no_of_conn  | integer   | creates parallel connections to connect to the server and send data - it must be 1 and the max value should be 5 - default:1                                                                                                         |
| -n   | --num      | no_of_bytes | string    | transfer number of bytes specfied by -n flag, it should be either in B, KB or MB                                                                                                                                                     |

If -c or -s flags are not specfied - you should print the following and exit:

    Error: you must run either in server or client mode

**NOTE:** When calculating the rate for the overall duration, measure
the time elapsed from when the client first starts sending data to
when it receives an ackonlowedgement (graceful close of connection)
message from the server.

**Running client with -i flag** 

When simpleperf is invoked in client mode
with -i flag, it will then print statistics per t seconds specified after the -i flag.

Here is an example:
```
python3 simpleperf -c -I <server_ip> -p <server_port> -t <time> -i 5

------------------------------------------------------------------------------------------
A simpleperf client connecting to server <IP>, port XXXX
------------------------------------------------------------------------------------------
Client connected with server_IP port XXXX
```

| ID        | Interval      | Transfer | Bandwith   |
|-----------|---------------|----------|------------|
| IP:port   | 0.0 - 5.0     | X MB     | Y Mbps     |
| IP:port   | 6.0 - 10.0    | X MB     | Y Mbps     |
| IP:port   | 11.0 - 15.0   | X MB     | Y Mbps     |
| IP:port   | 16.0 - 20.0   | X MB     | Y Mbps     |
| IP:port   | 21.0 - 25.0   | X MB     | Y Mbps     |
| --------- | ------------- | -------  | ---------- |
| IP:port   | 0.0 - 25.0    | X MB     | Y Mbps     |

**Running client with -n or --num flag** 
When simpleperf is invoked in client mode with -n flag, it will transfer the amount of bytes specified by -n and display the statistics

Here is an example:

    python3 simpleperf -c -I <server_ip> -p <server_port> -n 10M

The client will establish a TCP connection with the simpleperf server and send
10MB data in chunks of 1000 bytes. Simpleperf will calculate and display the
bandwidth.

**Running client with -P or --parallel flag**
The client will establish parallel TCP connection with the simpleperf server and send data in chunks of 1000 bytes for 100 seconds (specified with -t flag). At the end of the transfer,
Simpleperf client will calculate and display the bandwidth.

Here is an example where the client will open two TCP connections in parallel to connect with the server.

```
python3 simpleperf -c -I <server_ip> -p <server_port> -P 2 -t 100
------------------------------------------------------------------------------------------
A simpleperf client connecting to server <IP>, port XXXX
------------------------------------------------------------------------------------------
Client IP:port connected with server_IP port XXXX
Client IP: port connected with server_IP port XXXX
```
| ID        | Interval      | Transfer | Bandwith   |
|-----------|---------------|----------|------------|
| IP:port   | 0.0 - 25.0    | X MB     | Y Mbps     |
| IP:port   | 6.0 - 25.0    | X MB     | Y Mbps     |

**NOTE:** the arguments must not be positional arguments, i.e., users
do not need to remember the position of the argu