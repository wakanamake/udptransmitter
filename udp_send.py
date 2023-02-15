import socket
import ipaddress
import time
import random
import sys
import json
import signal
from struct import *

def handle_sigterm(signal, frame):
	print("\n")
	sock.close()
	sys.exit(0)

signal.signal(signal.SIGINT, handle_sigterm)

SIZE = 700
PREFIX = "172.12.0.0/24"
MAX_BW = 10
UDP_PORT = 5999
DST = "127.0.0.1"

args = sys.argv[1:]

if args:
	if "--prefix" in args:
		index = args.index("--prefix") + 1
		PREFIX = args[index]
	if "--port" in args:
		index = args.index("--port") + 1
		UDP_PORT = int(args[index])
	if "--bw" in args:
		index = args.index("--bw") + 1
		MAX_BW = int(args[index])
	if "--size" in args:
		index = args.index("--size") + 1
		SIZE = int(args[index])
	if "--dst" in args:
		index = args.index("--dst") + 1
		DST = args[index]

print(f"Target: {DST}:{UDP_PORT}, Source Prefix: {PREFIX}, MAX_Bandwidth: {MAX_BW}Mbps, Packet Size: {SIZE}Byte")


ip_list = []
network = ipaddress.IPv4Network(PREFIX)

for ip in network:
	ip_list.append(str(ip))

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)

start_time = time.time()
checker = time.time()
MAX_BW = MAX_BW * 1000 * 1000
sent_bytes = 0
sequence = 1
padding = "X" * SIZE


while True:
	Src = random.choice(ip_list)

	current_time = time.time()
	data = {'data': padding, 'timestamp': current_time, 'sequence': sequence}
	payload = json.dumps(data).encode()

	ip_header = b"\x45\x00\x00\x1d\x00\x00\x00\x00\x40\x11\x00\x00" + socket.inet_aton(Src) + socket.inet_aton(DST)

	udp_header = pack('!HHHH', UDP_PORT, UDP_PORT, 8+len(payload), 0)
	packet = ip_header + udp_header + payload

	sock.sendto(packet, (DST, UDP_PORT))

	if current_time - checker > 1:
		checker = current_time
		print(f"Packet Sent: {sequence}", end="\r")
	#print(sequence)

	sequence += 1

	sent_bytes += len(packet) + 14
	elapsed_time = time.time() - start_time
	expected_time = sent_bytes * 8 / MAX_BW
	time.sleep(max(0, expected_time - elapsed_time))
