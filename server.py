import json
import random
import socket
import pickle
from pprint import pprint

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Opening JSON file
f = open('data.json')
 
# Returns JSON object as a dictionary
data = json.load(f)

# Randomly choosing an object from the JSON file
sleuth = random.choice(data['sleuth_details'])

# Storing values from the chosen object in variables
# Storing puzzle theme as a string
#matrixTheme = [str(sleuth["theme"])]

# Storing the list of strings needed to create the puzzle
matrixList = []
matrixList = sleuth["matrix"]

# Storing the dictionary of words and their coordinate positions
wordsDict = {}
wordsDict = sleuth["words"]

# Creating a list out of the words dictionary keys to store the words in
wordsDictKeys = []
for key in wordsDict.keys():
    wordsDictKeys.append(key)

# Storing the maximum word count of the puzzle
wordCount = sleuth["count"]

# Initialising the received word
receiveWord = ""

# Starting connection and listening
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)
    print('server listening')
    
    # Accepting connection from Client
    conn, addr = s.accept()
    with conn:
        # Connection established
        print('Connected by', addr)
        while True:
            # Sending the list of strings to Client over TCP after pickling the object
            conn.send(pickle.dumps(matrixList))
            # Sending the word count to Client over TCP after pickling the object
            conn.send(pickle.dumps(wordCount))
            # Sending the list of matrix theme to Client over TCP after pickling the object
            #print(pickle.dumps(matrixTheme))
            #conn.send(pickle.dumps(matrixTheme))
            print("sent")
            # Words are received by Server and checked in a while loop until user guesses all words or presses "finish"
            while (receiveWord != "EXIT"):
                # Receiving word from Client and decoding it
                receiveWordByte = conn.recv(1024)
                receiveWord = receiveWordByte.decode("utf-8")
                print(receiveWord)
                # Checking if the word is present in the puzzle by comparing with dictionary keys
                if(receiveWord in wordsDict.keys()):
                    # If word is present, coordinates of the word in the puzzle are put into a list and sent to the Client over TCP
                    sendList = wordsDict[receiveWord]
                    print(sendList)
                    conn.send(pickle.dumps(sendList))
                else:
                    # If word is not present in the puzzle, it is checked if the word is EXIT or not
                    if(receiveWord != "EXIT"):
                        # If game has not ended yet, a list of just one element is sent to the Client over TCP
                        sendList = [0]
                        conn.send(pickle.dumps(sendList))
                    else:
                        # If received word is EXIT, game is over and this while loop is terminated
                        break

            missedWords = []

            # Receiving the list of all guessed words from Client over TCP and unpickling the object
            receiveListWordsByte = conn.recv(4096)
            receiveListWords = pickle.loads(receiveListWordsByte)
            print(receiveListWords)
            
            # Creating a list of the words that have not been guessed by the user by performing Set Difference Operation on the lists of Words Dictionary Keys and Received Words
            missedWords = list(set(wordsDictKeys) - set(receiveListWords))

            # Sending the list of missed words to the Client over TCP after pickling the object
            print(missedWords)
            print(pickle.dumps(missedWords))
            conn.send(pickle.dumps(missedWords))

            # The connection is closed
            break

# Closing file
f.close()
