import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = input("enter the roll number:")
# s.bind(('10.10.10.160',2020))
s.sendto(data.encode(),('10.10.10.160',2020))
data,conn = s.recvfrom(1024)
print(data.decode())
data,conn = s.recvfrom(1024)
print(data.decode())
s.close()