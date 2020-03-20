import socket
import os
import random
import functools
import threading



f = open("words.txt", "r")
allwords = f.read().split()
f.close()

def isguessed_word():
    '''if the letter guessed is in the alphabets and also in the secret word then 
    we will call another function choosed_word'''
    global data,c,answer
    if userInput in secretWord:
        data +=  'good guess:' + "\n" 
        '''After verifying that the letter is in the secret word we will iterate 
        through all the characters of the string and  find it's position and assign 
        that particular letter in the letters to be guessed and the game will continue'''
        for k in range(len(secretWord)):
            if secretWord[k] == userInput:
                answer[k] = userInput
    else:
        '''if the guessed letter is not in the secret word then one life will be 
        decreased and the game will continue '''
        c -= 1
        data += 'Oops!that letter is not in my word: ' + "\n"

def status():
    '''since we have to end the game if all the letters are guessed correctly 
    we will count the number of letters to be guessed after every attempt and 
    if the number is 0 then the loop will break  saying that he won!'''
    global data
    t = answer.count('_')
    if t==0:
        data += 'congratulations Game won!!' + "\n" + "secret Word is: " + secretWord + "\n"
        score = calculateScore()
        player.playerScore += score
        data += "Your score is: " + str(score) + "\n" + getLeaderBoard() + "\n"
        return 1
    if c==0:
        score = calculateScore()
        player.playerScore += score
        data += 'sorry you have run out of lives.The word is ' + secretWord + "\n your score is "  + str(score) + "\n Game Lost " + "\n" + getLeaderBoard() + "\n"
        conn.sendall(data.encode())
        return 1
    return 0

def comparator(x,y):
    if(allUsers[x].playerScore > allUsers[y].playerScore):
        return -1
    elif(allUsers[x].playerScore == allUsers[y].playerScore):
        if(x > y):
            return -1
    return 1

def getLeaderBoard():
    leaderBoard = sorted(allUsers, key=functools.cmp_to_key(comparator))
    dump = ""
    for i in leaderBoard:
        dump +=  i + "\t" + str(allUsers[i].playerScore) + "\n"
    return dump

def calculateScore():
    return (10 * len(secretWord)) - ((6 - c) * (len(secretWord)))


class Player:
    playerScore = 0
    wordsUsed = []
    def __init__(self,Secretword):
        super().__init__()
        self.wordsUsed.append(Secretword)

def serveRequest(conn,addr):
    global data,player,secretWord,allUsers,answer,alphabets,userInput
    print("connection is: " , addr)
    data = "Welcome to Hangman." + "\n" + "enter the value based on the following" + "\n" + "newUser = 1" + "\n" + "oldUser = 0"
    conn.send(data.encode())
    temp = 1
    while temp:
        data = conn.recv(1024)
        data = data.decode()
        # if(data == "quit"):
        #     break
        if(data == "0"):
            conn.send(b'enter userName')
            while 1:
                data = conn.recv(1024)
                data = data.decode()
                if(data == "1"):
                    break
                if(data in allUsers):
                    player = allUsers[data]
                    while 1:
                        secretWord = random.choice(allwords)
                        if(secretWord not in player.wordsUsed):
                            player.wordsUsed.append(secretWord)
                            break
                    temp = 0
                    break
                else:
                    conn.send(b'user not available try again.Enter 1 to register as new player')

                if(temp == 0):
                    break
        if(data == "1"):
            conn.send(b'Enter User name')
            while 1:
                data = conn.recv(1024)
                data = data.decode()
                if(data in allUsers):
                    conn.send(b"UserName not available.Try another name")
                else:
                    secretWord = random.choice(allwords)
                    # data = Player(secretWord)
                    allUsers[data] = Player(secretWord)
                    player = allUsers[data]
                    temp = 0
                    break
        if(temp == 1):
            data = "enter 0 or 1"
            conn.send(data.encode())
    temp =  1
    data = "user created succesfully." + "\n"

    c = 6
    alphabets = []
    for i in range(26):
        alphabets.append(chr(i+97))
    
    l = len(secretWord)
    answer = ['_']*l
    print("secretWord is: ",secretWord)
    while temp:
        data += 'length of the word is: ' + str(l) + "\n" + 'guess the word: ' + (' '.join(answer)) + "\n" + 'Available letters: ' + (','.join(alphabets))+ "\n" + 'you have ' + str(c) + ' chances'  + "\n"
        conn.sendall(data.encode())
        userInput = conn.recv(1024).decode()
        userInput = userInput.lower()
        data = "------------------------------------" + "\n"
        if userInput in alphabets:
            '''we will verify if the guessed letter is in alphabets and remove it accordingly'''
            alphabets.remove(userInput)
            isguessed_word()
        else:
            data += 'oops! you have already guessed that letter.try again: ' + (' '.join(answer))
        flag = status()
        if flag:
            conn.sendall(data.encode())
            temp = 0
            conn.close()



secretWord = ""
allUsers = {}
player = ""
userInput = ""
data = ""
answer = ""
alphabets = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('',8888))
sock.listen()
print('server started')
while 1:
    conn,addr = sock.accept()
    c = 6
    threading.Thread(target = serveRequest, args = (conn,addr)).start()

