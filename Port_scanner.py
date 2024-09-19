#!/bin/python3
import sys
import socket
from datetime import datetime

#define our target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #translate hostname to IPv4
else:
	print("invalid amount of arg.")
	print("syntax: python3 scanner.py <ip>")
	
#add a pretty banner
print("-" * 50)
print("scanning target: " + target)
print("time started: " +str(datetime.now()))
print("-" * 50)

try:	
	for port in range(50,85):
		s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		result= s.connect_ex((target,port)) #return an error indicator
		print("Checking port number {}".format(port))
		if result == 0:
			print("port {} is open.".format(port))
		s.close()

except KayboardInterrupt:
	print("\nExiting porgram.")
	sys.exit()
	
except socket.gaierror:
	print("hostname could not be resolved.")
	
except socket.error:
	print("couldn't connect to server.")
	sys.exit()
