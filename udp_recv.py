import socket
import sys
import json
import time
import select
import signal
import os

os.nice(-20)

UDP_IP = "0.0.0.0"
UDP_PORT = 5999
RECV_BUF = 8192 * 1024
NUM_WORKERS = 2

received_packets = 0
dropped_packets = 0

def signal_handler(sig, frame):
	print(f"\nReceived: {received_packets}, Droped: {dropped_packets}, Latency(min): {min_latency * 1000:.3f}ms, Latency(avg): {avg_latency * 1000:.3f}ms, Latency(max): {max_latency * 1000:.3f}ms")
	sock.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

args = sys.argv[1:]

if args:
	if "--port" in args:
		index = args.index("--port") + 1
		UDP_PORT = int(args[index])

print(f"Listen on: {UDP_PORT}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))

min_latency = float('inf')
max_latency = float('-inf')
latency_sum = float(0)
avg_latency = float(0)
max_sequence = 0
checker = time.time()

inputs = [sock]

while True:
	readable, writable, exceptional = select.select(inputs, [], [], 0.1)
	for s in readable:
		if s is sock:

			data, addr = sock.recvfrom(1600)
			received_packets += 1

			json_data = json.loads(data.decode())

			current_time = time.time()
			sent_time = json_data['timestamp']
			sequence = json_data['sequence']

			if sequence > max_sequence:
				max_sequence = sequence
			dropped_packets = max_sequence - received_packets

			latency = current_time - sent_time
			latency_sum += latency

			if latency < min_latency:
				min_latency = latency
			if latency > max_latency:
				max_latency = latency
			avg_latency = latency_sum / received_packets

			if current_time - checker > 1:
				checker = current_time
				print(f"Received: {received_packets}, Droped: {dropped_packets}, Latency(min): {min_latency * 1000:.3f}ms, Latency(avg): {avg_latency * 1000:.3f}ms, Latency(max): {max_latency * 1000:.3f}ms", end="\r")