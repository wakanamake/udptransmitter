import socket
import sys
import json
import time
import statistics

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

latencies = []

while True:
	data, addr = sock.recvfrom(4096)

	json_data = json.loads(data.decode())

	current_time = time.time()
	sent_time = json_data['timestamp']

	latency = current_time - sent_time
	latencies.append(latency)

	min_latency = min(latencies)
	avg_latency = statistics.mean(latencies)
	max_latency = max(latencies)

	print(f"Minimum latency: {min_latency:.6f}, Average latency: {avg_latency:.6f}, Maximum latency: {max_latency:.6f}", end="\r")

	#print("Rcv from {}:{}".format(addr, latency))

sock.close()