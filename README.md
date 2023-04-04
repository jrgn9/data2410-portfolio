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

## How to run
Simpleperf runs in server and client mode. Each mode have different flags you can invoke.

**To get the full list of every flag you can run:**

```
python simpleperf.py -h
```

&nbsp;

**To run server mode with default values:**
```
python simpleperf.py -s
```
*Will run the server on 127.0.0.1:8088 printing in MB format.* 

&nbsp;

**To run the client mode with default values:**
```
python simpleperf.py -c
```
*Will run the client with 127.0.0.1:8088 as server, printing in MB format and run for 25 seconds.*

&nbsp;

## Sources:
https://docs.python.org/3/library/argparse.html

https://docs.python.org/3/library/re.html

https://github.com/safiqul/2410

https://pypi.org/project/prettytable/

https://www.techwithtim.net/tutorials/socket-programming/

Labs and lectures

Some help with troubleshooting from ChatGPT - https://chat.openai.com