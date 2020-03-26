import socket
import random
import functools
import threading

f = open("words.txt", "r")
allwords = f.read().split()
f.close()

class Hangman:
    """This is a class for Hangman Game."""

    class Player:
        """
        This is a class for Player who has the score obtained and words guessed.
        
        Attributes: 
            secretword(String):Randomly generated word.

        """

        playerScore = 0
        wordsUsed = []
        def __init__(self,Secretword):
            """ 
            The constructor for Player class. 
    
            Parameters: 
                secretword(String):Randomly generated word.  
            
            """

            super().__init__()
            self.wordsUsed.append(Secretword)

    def __init__(self):
        """The constructor for Hangman class."""

        super().__init__()
        self.allUsers = {}
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('127.0.0.1',8888))
        sock.listen()
        print('server started')
        while 1:
            print('allUsers: ',  self.allUsers)
            conn,addr = sock.accept()
            try:
                threading.Thread(target = self.serveRequest, args = (conn,addr)).start()
            except Exception:
                exit()

    def serveRequest(self,conn,addr):
        """ 
        The function to start the thread for the given conn,addr. 
  
        Parameters: 
            conn (Conn): The response to be sent to.
            addr (tup) : The address of the conn.
          
        """
        
        secretWord = ""
        player = ""
        userInput = ""
        data = ""
        answer = ""
        alphabets = []
        userName = ""
        chances = 6
        
        def isguessed_word():
            """
            If the letter guessed is in the alphabets and also in the secret word then 
            we will call another function choosed_word
            
            """
            
            nonlocal data,chances,answer
            if userInput in secretWord:
                data +=  'good guess:' + "\n"
                """After verifying that the letter is in the secret word we will iterate
                through all the characters of the string and  find it's position and assign
                that particular letter in the letters to be guessed and the game will continue.
                
                """
                
                for k,l in enumerate(secretWord):
                    if l == userInput:
                        answer[k] = userInput
            else:
                """If the guessed letter is not in the secret word then one life will be
                decreased and the game will continue.
                """
                
                chances -= 1
                data += 'Oops!that letter is not in my word.Try again. ' + "\n"

        def status():
            """since we have to end the game if all the letters are guessed correctly
            we will count the number of letters to be guessed after every attempt and
            if the number is 0 then the loop will break  saying that he won!."""
            nonlocal data,player
            t = answer.count('_')
            if t == 0:
                if (userName not in self.allUsers):
                    self.allUsers[userName] = self.Player(secretWord)
                    player = self.allUsers[userName]
                data += 'congratulations Game won!!' + "\n" + "secret Word is: " + secretWord + "\n"
                score = calculateScore()
                player.playerScore += score
                data += "Your score is: " + str(score) + "\n" + getLeaderBoard() + "\n"
                return 1
            if chances == 0:
                if (userName not in self.allUsers):
                    self.allUsers[userName] = self.Player(secretWord)
                    player = self.allUsers[userName]
                score = calculateScore()
                player.playerScore += score
                data += 'sorry you have run out of lives.The word is ' + secretWord + "\n your score is "  + str(score) + "\n Game Lost " + "\n" + getLeaderBoard() + "\n"
                conn.sendall(data.encode())
                return 1
            return 0

        def comparator(x,y):
            if(self.allUsers[x].playerScore > self.allUsers[y].playerScore):
                return -1
            elif(self.allUsers[x].playerScore == self.allUsers[y].playerScore):
                if(x > y):
                    return -1
            return 1

        def getLeaderBoard():
            leaderBoard = sorted(self.allUsers, key=functools.cmp_to_key(comparator))
            print("leaderboard:  " , player)
            dump = "Leaderboard: \n \t name \t score \n"
            for i in leaderBoard:
                dump +=  "\t" + i + "\t" + str(self.allUsers[i].playerScore) + "\n"
            return dump

        def calculateScore():
            return (10 * len(secretWord)) - ((6 - chances) * (len(secretWord)))

        print("connection is: " , addr)
        data = "Welcome to Hangman." + "\n" + "enter the value based on the following" + "\n" + "newUser = 1" + "\n" + "oldUser = 0"
        conn.send(data.encode())
        temp = 1
        while temp:
            data = conn.recv(1024)
            data = data.decode()
            if(data == "0"):
                conn.send(b'enter userName')
                while 1:
                    data = conn.recv(1024)
                    data = data.decode()
                    if(data == "1"):
                        break
                    if(data in self.allUsers):
                        userName = data
                        player = self.allUsers[data]
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
                    if(data in self.allUsers):
                        conn.send(b"UserName not available.Try another name")
                    else:
                        secretWord = random.choice(allwords)
                        userName = data
                        temp = 0
                        break
            if(temp == 1):
                data = "enter 0 or 1"
                conn.send(data.encode())
        temp =  1
        data = "user created succesfully." + "\n"
        
        for i in range(26):
            alphabets.append(chr(i+97))

        length = len(secretWord)
        answer = ['_']*length
        print("secretWord is: ",secretWord)
        while temp:
            data += 'length of the word is: ' + str(length) + "\n" + 'guess the word: ' + (' '.join(answer)) + "\n" + 'Available letters: ' + (','.join(alphabets))+ "\n" + 'you have ' + str(chances) + ' chances'  + "\n"
            conn.sendall(data.encode())
            userInput = conn.recv(1024).decode()
            userInput = userInput.lower()
            data = "------------------------------------" + "\n"
            if userInput in alphabets:
                """we will verify if the guessed letter is in alphabets and remove it accordingly"""

                alphabets.remove(userInput)
                isguessed_word()
            else:
                data += 'oops! you have already guessed that letter.try again: ' + "\n"
                #  + (' '.join(answer))
            flag = status()
            if flag:
                conn.sendall(data.encode())
                temp = 0
                conn.close()

Hangman()