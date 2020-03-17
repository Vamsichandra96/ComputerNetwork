import random


uploaded = files.upload()
contents = uploaded['words.txt'].split()
alphabets = []
for i in range(26):
    alphabets.append(chr(i+97))

def available_letters():
  
  '''we will verify if the guessed letter is in alphabets and remove it accordingly'''
  global alphabets
  alphabets.remove(i)
  t1_join = ','.join(alphabets)
  return t1_join

def isguessed_word():
  '''if the letter guessed is in the alphabets and also in the secret word then 
  we will call another function choosed_word'''
  if i in a:
    print('good guess:',choosed_word())
  else:
    notguessed_word()
        
def notguessed_word():
  '''if the guessed letter is not in the secret word then one life will be 
  decreased and the game will continue '''
  global c
  c = c-1
  print('Oops!that letter is not in my word:%s' %' '.join(answer) )
    
    

def choosed_word():
  '''After verifying that the letter is in the secret word we will iterate 
  through all the characters of the string and  find it's position and assign 
  that particular letter in the letters to be guessed and the game will continue'''
  for k in range(l):
    if a[k] == i:
      answer[k] = i
  t2_join = ' '.join(answer)
  return t2_join

def status():
  '''since we have to end the game if all the letters are guessed correctly 
  we will count the number of letters to be guessed after every attempt and 
  if the number is 0 then the loop will break  saying that he won!'''
  t = answer.count('_')
  if t==0:
      print('congratulations you won!!')
      return 1
    
    

a = random.choice(contents).decode("utf-8")
l = len(a)
print(a)
print('welcome to hangman game')
c = l
answer = ['_']*l
print(f'length of the word is:{l}')
print('guess the word:%s'%(' '.join(answer)))
print('Available letters:%s'%(','.join(alphabets)))
print(f'you have {c} chances')
      
while True:
  i = str(input('please guess a letter:'))
  i = i.lower()
  if len(i) == 1 and (ord(i) >= 97 and ord(i) <= 122):
    if i in alphabets:
      available_letters()
      x = isguessed_word()
    else:
      print('oops! you have already guessed that letter.try again:%s' %(' '.join(answer)))
  else:
     print('only single letter from a to z is accepted:%s' %(' '.join(answer)))
  temp = status()
  if temp:
    break
  print('\n')
  print('guess the word:%s' %(' '.join(answer)))
  print(f'you have {c} chances')
  print(','.join(alphabets))
  if c==0:
    break
  
    
# if the person used all his lives we will print the following statement
if c == 0:
  print(f'sorry you have run out of lives.The word is {a}')
