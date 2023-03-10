import time       # let's time our script

import ipaddress  # https://docs.python.org/3/library/ipaddress.html
                  # convert ip/mask to list of hosts


import subprocess # https://docs.python.org/3/library/subprocess.html
                  # to make a popup window quiet

from colorama import init  # colors https://en.wikipedia.org/wiki/ANSI_escape_code
init()                     # https://pypi.org/project/colorama/


import threading           # for threading functions, lock, queue
from queue import Queue    # https://docs.python.org/3/library/queue.html

# define a lock that we can use later to keep
# prints from writing over itself
print_lock = threading.Lock()

# Prompt the user to input a network address
net_addr = input("Enter Network (192.168.1.0/24): ")

# actual code start time
startTime = time.time()

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

# quick message/update
print ('Sweeping Network with ICMP: ', net_addr)

# the actual ping definition and logic.
# it's called from a pool, repeatedly threaded, not serial
def pingsweep(ip):
    
    # for windows:   -n is ping count, -w is wait (ms)
    # for linux: -c is ping count, -w is wait (ms)
    # I didn't test subprocess in linux, but know the ping count must change if OS changes

    output = subprocess.Popen(['ping', '-n', '1', '-w', '150', str(all_hosts[ip])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
    
    # lock this section, until we get a complete chunk
    # then free it (so it doesn't write all over itself)
    with print_lock:
      
      # normalize colors to grey
      print('\033[93m', end='')

      # code logic if we have/don't have good response
      if "Reply" in output.decode('utf-8'):
         print(str(all_hosts[ip]), '\033[32m'+"is Online")
      elif "Destination host unreachable" in output.decode('utf-8'):
         #print(str(all_hosts[ip]), '\033[90m'+"is Offline (Unreachable)")
         pass
      elif "Request timed out" in output.decode('utf-8'):
         #print(str(all_hosts[ip]), '\033[90m'+"is Offline (Timeout)")
         pass
      else:
         # print colors in green if online
         print("UNKNOWN", end='')

# defines a new ping using def pingsweep for each thread
# holds task until thread completes
def threader():
   while True:
      worker = q.get()
      pingsweep(worker)
      q.task_done()
      
q = Queue()

# up to 100 threads, daemon for cleaner shutdown   
# just spawns the threads and makes them daemon mode
for x in range(100):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()

# loops over the last octet in our network object
# passing it to q.put (entering it into queue)
for worker in range(len(all_hosts)):
   q.put(worker)

# queue management   
q.join()

# ok, give us a final time report
runtime = float("%0.2f" % (time.time() - startTime))
print("Run Time: ", runtime, "seconds")
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
import time       # let's time our script
 
import ipaddress  # https://docs.python.org/3/library/ipaddress.html
                  # convert ip/mask to list of hosts
 
 
import subprocess # https://docs.python.org/3/library/subprocess.html
                  # to make a popup window quiet
 
from colorama import init  # colors https://en.wikipedia.org/wiki/ANSI_escape_code
init()                     # https://pypi.org/project/colorama/
 
 
import threading           # for threading functions, lock, queue
from queue import Queue    # https://docs.python.org/3/library/queue.html
 
# define a lock that we can use later to keep
# prints from writing over itself
print_lock = threading.Lock()
 
# Prompt the user to input a network address
net_addr = input("Enter Network (192.168.1.0/24): ")
 
# actual code start time
startTime = time.time()
 
# Create the network
ip_net = ipaddress.ip_network(net_addr)
 
# Get all hosts on that network
all_hosts = list(ip_net.hosts())
 
# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE
 
# quick message/update
print ('Sweeping Network with ICMP: ', net_addr)
 
# the actual ping definition and logic.
# it's called from a pool, repeatedly threaded, not serial
def pingsweep(ip):
    
    # for windows:   -n is ping count, -w is wait (ms)
    # for linux: -c is ping count, -w is wait (ms)
    # I didn't test subprocess in linux, but know the ping count must change if OS changes
 
    output = subprocess.Popen(['ping', '-n', '1', '-w', '150', str(all_hosts[ip])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
    
    # lock this section, until we get a complete chunk
    # then free it (so it doesn't write all over itself)
    with print_lock:
      
      # normalize colors to grey
      print('\033[93m', end='')
 
      # code logic if we have/don't have good response
      if "Reply" in output.decode('utf-8'):
         print(str(all_hosts[ip]), '\033[32m'+"is Online")
      elif "Destination host unreachable" in output.decode('utf-8'):
         #print(str(all_hosts[ip]), '\033[90m'+"is Offline (Unreachable)")
         pass
      elif "Request timed out" in output.decode('utf-8'):
         #print(str(all_hosts[ip]), '\033[90m'+"is Offline (Timeout)")
         pass
      else:
         # print colors in green if online
         print("UNKNOWN", end='')
 
# defines a new ping using def pingsweep for each thread
# holds task until thread completes
def threader():
   while True:
      worker = q.get()
      pingsweep(worker)
      q.task_done()
      
q = Queue()
 
# up to 100 threads, daemon for cleaner shutdown   
# just spawns the threads and makes them daemon mode
for x in range(100):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()
 
# loops over the last octet in our network object
# passing it to q.put (entering it into queue)
for worker in range(len(all_hosts)):
   q.put(worker)
 
# queue management   
q.join()
 
# ok, give us a final time report
runtime = float("%0.2f" % (time.time() - startTime))
print("Run Time: ", runtime, "seconds")