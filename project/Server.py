import socket
import os
class player:
    playerScore = 0
    wordsUsed = []
    def __init__(self,Secretword):
        super().__init__()
        self.wordsUsed.append(Secretword)

allUsers = []
player = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('127.0.0.1',8888))
sock.listen()
print('server created')
while 1:
    conn = sock.accept()
    print("connection is: " , conn)
    data = "Welcome to Hangman." + "\n"
    data += "enter the value based on the following" + "\n" + "newUser = 1" + "\n" + "oldUser = 0"
    conn.sendall(data.encode())
    temp = 1
    while temp:
        data = conn.recv(1024)
        data = data.decode()
        if(data == "0"):
            conn.send('enter userName')
            while 1:
                data = conn.recv(1024)
                data = data.decode()
                if(data == "1"):
                    break
                if(data in allUsers):
                    player = allUsers[data]
                    temp = 0
                    break
                else:
                    conn.send(b'user not available try again.Enter 1 to register as new player')
        elif(data == "1"):
            conn.send(b'Enter User name')
            while 1:
                data = conn.recv(1024)
                data = data.decode()
                if(data in allUsers):
                    conn.send("UserName not available.Try again")
                else:
                    allUsers[data] = player("secretWord")
                    break
        else:
            data = "enter 0 or 1"
            conn.send(data.encode())
    conn.send(b'user created succesfully.')
    data = conn.recv(1024)
    data = data.upper()
    conn.sendto(data.encode(),conn)
    conn.close() 
