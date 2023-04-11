# SIMPLEPERF

Simpleperf is a program based on the iPerf tool for measuring network throughput. This program is a simplified network throughput measurement tool. simpleperf sends and recieves packets of 1000 bytes between a client and a server using sockets. It runs in two modes: Server mode and client mode.

## Dependencies
This program uses [PrettyTable](https://pypi.org/project/prettytable/) as a dependency.
To install via [pip](https://pip.pypa.io/en/stable/installation/):

```
python -m pip install -U prettytable
```

If **ModuleNotFoundError** try instead to install the tarball prettytable-3.6.0.tar.gz in this repository:
```
sudo pip install ./prettytable-3.6.0.tar.gz
```
*You might have to run with --force-reinstall for this to work*

### Troubleshooting:

I sometimes had some difficulties running PrettyTable in xterm. For the most part, just importing it with the tarball did the trick. However, sometimes I had to just purge pip completely and start over.

```
sudo apt-get --purge autoremove python3-pip
sudo apt-get update && sudo apt-get install python3-pip
```

 I don't know if it works best to install pip and the library right in xterm or in bash terminal, but I would try both approaches if it doesn't work. I would also check if there are a more recent version than 3.6.0 and download a new tarball if it is giving you trouble. After some purging and cursing it have always worked for me.

## How to run
Simpleperf runs in server and client mode. Each mode have different flags you can invoke.

**To get the full list of every flag you can run:**

```
python simpleperf.py -h
```

**To run server mode with default values:**
```
python simpleperf.py -s
```
*Will run the server on 127.0.0.1:8088 printing in MB format.* 


**To run the client mode with default values:**
```
python simpleperf.py -c
```
*Will run the client with 127.0.0.1:8088 as server, printing in MB format and run for 25 seconds.* 

&nbsp;

### **Table below lists all the available options that you can use to invoke the server:**

| **flag** | **long flag** | **input**   | **type**  | **description**                                                                                                                                                                                       |
|:--------:|:-------------:|:-----------:|:---------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| -s       | --server      | X           | boolean | enable the server mode                                                                                                                                                                                |
| -b       | --bind        | ip address   | string    | allows to select the ip address of the server’s interface where the client should connect. It must be in the dotted decimal notation format, e.g. 10.0.0.2. Default value if no address is provided: 127.0.0.1 |
| -p       | --port        | port number | integer   | allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088                                                         |
| -f       | --format      | data type          | string    | allows you to choose the format of the summary of results - it must be either in B, KB or MB. default: MB   

&nbsp;

### **Table below lists all the available options that you can use to invoke the client:**

| flag | long flag  | input       | type      | description                                                                                                                                                                                                                          |
|------|------------|-------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -c   | --client   | X           | boolean | enable the client mode                                                                                                                                                                                                               |
| -I   | --serverip | ip adress   | string    | allows to select the ip address of the server. It must be in the dotted decimal notation format, e.g. 10.0.0.2. Default value if no address is provided: 127.0.0.1                                                                            |
| -p   | --port     | port number | integer   | allows to use select port number on which the server should listen; the port must be an integer and in the range [1024, 65535], default: 8088                                                                                        |
| -t   | --time     | seconds     | integer   | the total duration in seconds for which data should be generated, also sent to the server (if it is set with -t flag at the client side) and must be > 0. If nothing is set, default: 25 seconds |
| -f   | --format   | Data type         | string    | allows you to choose the format of the summary of results - it must be either in B, KB or MB. Default: MB                                                                                                                          |
| -i   | --interval | X           | integer   | print statistics per X second                                                                                                                                                                                                        |
| -P   | --parallel | number of connections  | integer   | creates parallel connections to connect to the server and send data - it must be 1 and the max value is 5 - default:1                                                                                                         |
| -n   | --num      | number of bytes | string    | transfer number of bytes specified by -n flag, it must be either in B, KB or MB                                                                                                                                                     |

&nbsp;

## Sources:
Sources used in this code. Most of it are python documentation and code from lecturer.

https://docs.python.org/3/library/argparse.html

https://docs.python.org/3/library/re.html

https://github.com/safiqul/2410

https://pypi.org/project/prettytable/

https://www.techwithtim.net/tutorials/socket-programming/

Labs and lectures

Some help with troubleshooting from ChatGPT - https://chat.openai.com