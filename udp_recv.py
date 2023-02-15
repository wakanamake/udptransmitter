import socket
import sys

UDP_IP = "0.0.0.0"
UDP_PORT = 5999

args = sys.argv[1:]

if args:
	if "--port" in args:
		index = args.index("--port") + 1
		UDP_PORT = int(args[index])

print(f"Listen on: {UDP_PORT}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(4096)
	# DEBUG
	#print("Rcv from {}:{}".format(addr, data.decode()))

sock.close()
