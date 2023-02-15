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
#sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))

min_latency = float('inf')
max_latency = float('-inf')
latency_sum = float(0)

max_sequence = 0

latencies = []
sequences = []
checker = time.time()
count = 1

while True:
	try:
		data, addr = sock.recvfrom(2048)

		json_data = json.loads(data.decode())

		current_time = time.time()
		sent_time = json_data['timestamp']
		sequence = json_data['sequence']

		if sequence > max_sequence:
			max_sequence = sequence
		#sequences.append(sequence)

		latency = current_time - sent_time
		latency_sum += latency

		if latency < min_latency:
			min_latency = latency
		if latency > max_latency:
			max_latency = latency
		avg_latency = latency_sum / count

		if current_time - checker > 1:
			checker = current_time
			print(f"Received: {count}, Droped: {max_sequence-count}, Latency(min): {min_latency * 1000:.3f}ms, Latency(avg): {avg_latency * 1000:.3f}ms, Latency(max): {max_latency * 1000:.3f}ms", end="\r")
		count += 1

	except BlockingIOError:
		pass