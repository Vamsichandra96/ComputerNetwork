import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = "Hello World"
s.sendto(data.encode(),('10.1.40.37',2020))
data,conn = s.recvfrom(1024)
print(data.decode())
s.close() 