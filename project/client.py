import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.connect(('127.0.0.1',8888))
print(sock.recv(1024).decode())
while 1:
    sock.send(input().encode())
    data = sock.recv(1024).decode()
    if("Game Lost" in data or "Game won!!" in data):
        print(data)
        break
    print(data)
