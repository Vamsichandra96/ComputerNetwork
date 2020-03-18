import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.connect(('127.0.0.1',8888))
temp = 1
print(sock.recv(1024).decode())
while temp:
    sock.send(input().encode())
    data = sock.recv(1024).decode()
    print(data)
    if(data == "user created succesfully."):
        break

print("outside the client.")