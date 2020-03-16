import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('10.10.10.160',2020))
print('server created')
while 1:
    data,conn = s.recvfrom(1024)
    print("connection is: " , conn)
    data = data.decode()
    data = data.upper()
    s.sendto(data.encode(),conn)
s.close()