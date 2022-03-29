import socket
import pickle
from tkinter import *
import pyglet, os

# If pyglet is not already installed, use this command: python -m pip install pyglet

# Using pyglet to add a custom font
pyglet.font.add_file('Digital-7.ttf')

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# Initialising global variables
BACKGROUND_COLOR = "#B1DDC6"
SCORE = 0

# Creating root window
root = Tk()
root.title("WORD SLEUTH")
root.geometry("1700x956")

# Setting background image for the root window
mainbg = PhotoImage(file = "images/first.png")
bgLabel = Label(root, image = mainbg)
bgLabel.place(relx=0.5, rely=0.5, anchor='center')

# Function to start a new game
def openGameWindow():
    gameWindow = Toplevel(root)
    gameWindow.title("WORD SLEUTH")
    gameWindow.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
    # Class definition to display the matrix of letters in the puzzle as a table
    class Table:     
        def __init__(self,frame3): 
            for i in range(total_rows): 
                for j in range(total_columns):
                    # Creating text boxes and inserting the appropriate letter in them
                    self.e = Text(frame3, width=2, height=1, fg='blue', bd=0, font=('Arial',10,'bold')) 
                    self.e.grid(row=i, column=j) 
                    self.e.insert(END, receiveMatrixList[i][j])
                    self.e.configure(state='disabled')
        # Function to highlight a letter if its coordinates in the matrix are given
        def color(self,frame3,row,col):
            self.e = Text(frame3, width=2, height=1, fg='red', bd=0,bg="#FFF79F", font=('Arial',10,'bold')) 
            self.e.grid(row=row, column=col) 
            self.e.insert(END, receiveMatrixList[row][col])
            self.e.configure(state='disabled')

    # Establishing connection with Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
    
        # Receiving the list of strings required the make the puzzle from the Server over TCP and unpickling the object
        data = s.recv(4096)
        receiveMatrixList = pickle.loads(data)
        print(receiveMatrixList)

        # Find total number of rows and columns in the matrix to create the table 
        total_rows = len(receiveMatrixList) - 1
        total_columns = len(receiveMatrixList[0])

        matrixTheme = ""

        # # Receiving the word count of the puzzle from the Server over TCP and unpickling the object
        wordCountByte = s.recv(4096)
        wordCount = pickle.loads(wordCountByte)
        print(wordCount)

        # Receiving the list of string which is the matrix theme from the Server over TCP and unpickling the object
        #themeByte = s.recv(4096)
        #matrixtheme = pickle.loads(themeByte)
        matrixtheme = receiveMatrixList[20]
        print(matrixtheme)

        # Declaring variables
        inputWords = []                 # Maintains list of words entered by the user
        inputWord = "none"
        inp = "none"
        receiveMissedWords = []

        # Frame 1 is on the left half of the Game Window
        frame1=Frame(gameWindow,width=551,height=900,bg=BACKGROUND_COLOR,pady=0)
        frame1.grid(row=0,column=0)

        # Creating a Canvas in Frame 1 to display the background image for the matrix
        canvas = Canvas(frame1,width=420, height=450)
        canvas.pack(padx=50,pady=50)
        card_front_img = PhotoImage(file="images/card_front.png")
        card_background = canvas.create_image(210, 225, image=card_front_img)
        canvas.image = card_front_img
        canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        canvas.grid(row=1, column=0)

        # Frame 2 is the top frame inside Frame 1 and contains the theme of the puzzle
        frame2=Frame(frame1,width=500,height=100,bg=BACKGROUND_COLOR,pady=20)
        frame2.grid(row=0,column=0)

        # Assigning image to label, which is inserted in the frame and works as a background
        theme_img = PhotoImage(file="images/theme.png")
        theme_label = Label(frame2, text=matrixtheme, image=theme_img, compound='center',font=('Constantia',10),wraplength=450,padx=10)
        theme_label.image = theme_img
        theme_label.place(relx=0.5, rely=0.5, anchor='center')

        # Frame 3 is the second frame inside Frame 1 and is on top of the canvas, it displays the matrix table
        frame3=Frame(frame1,width=400,height=400,bg="#297931")
        frame3.grid(row=1,column=0)

        # Frame 4 is the third frame inside Frame 1 and it contains the Input Text Box and the two buttons to Enter the word and Finish the game
        frame4=Frame(frame1,width=400,height=100,bg=BACKGROUND_COLOR,pady=20)
        frame4.grid(row=2,column=0)

        # Frame 5 is on the right half of the Game Window
        frame5=Frame(gameWindow,width=500,height=900,bg=BACKGROUND_COLOR,padx=30)
        frame5.grid(row=0,column=1)

        # Frame 6 is the top frame inside Frame 5 and it contains the score obtained by the user so far
        frame6=Frame(frame5,width=200,height=200,bg=BACKGROUND_COLOR,pady=0)
        frame6.grid(row=0,column=0)

        # Assigning image to label, which is inserted in the frame and works as a background
        score_card_img = PhotoImage(file="images/score_card.png")
        score_img_label = Label(frame6, text=str(SCORE), image=score_card_img, compound='center', fg="#FFF79F",font=('Digital-7',40))
        score_img_label.img = score_card_img
        score_img_label.place(relx=0.5, rely=0.5, anchor='center')

        # A label to show the title "guessed words"
        guessed_words_title = Label(frame5, text="GUESSED WORDS:",bg="#eb8a8a",compound='center',font=('Constantia',15))
        guessed_words_title.grid(row=1,column=0)

        # Frame 7 is the middle frame inside Frame 5 and it continuously updates the list of words guessed by the user
        frame7=Frame(frame5,width=400,height=210,pady=30)
        frame7.grid(row=2,column=0)

        # Assigning image to label, which is inserted in the frame and works as a background
        guessed_words_img = PhotoImage(file="images/guessed_words_bg.png")
        guessed_words_label = Label(frame7, text=inputWords, image=guessed_words_img, compound='center',font=('Constantia',10),wraplength=380)
        guessed_words_label.img = guessed_words_img
        guessed_words_label.place(relx=0.5, rely=0.5, anchor='center')

        # A label to show the title "missed words"
        missed_words_title = Label(frame5, text="MISSED WORDS:",bg="#eb8a8a",compound='center',font=('Constantia',15))
        missed_words_title.grid(row=3,column=0)

        # Frame 8 is the botton frame inside Frame 5 and it shows the list of words missed by the user once game is over
        frame8=Frame(frame5,width=400,height=210,pady=30)
        frame8.grid(row=4,column=0)

        # Assigning image to label, which is inserted in the frame and works as a background
        missed_words_img = PhotoImage(file="images/guessed_words_bg.png")
        missed_words_label = Label(frame8, text=receiveMissedWords, image=guessed_words_img, compound='center',font=('Constantia',10),wraplength=380)
        missed_words_label.img = missed_words_img
        missed_words_label.place(relx=0.5, rely=0.5, anchor='center')#,padx=10,pady=10)

        # Frame 9 is the fourth frame inside Frame 1 and it shows the user messages indicating whether the entered word is present in the puzzle or not, or if the user has already entered the word
        frame9=Frame(frame1,width=500,height=136,pady=10)
        frame9.grid(row=3,column=0)

        # Assigning image to label, which is inserted in the frame and works as a background
        message_img = PhotoImage(file="images/message.png")
        message_label = Label(frame9, text="Welcome! Type words in the input box and press the green button. Press finish button to end the game.", image=message_img, compound='center',fg="green",font=('Constantia',15),wraplength=460)
        message_label.img = message_img
        message_label.place(relx=0.5, rely=0.5, anchor='center')

        # Putting the table inside Frame 3
        t = Table(frame3)

        #Input TextBox Creation
        inputtxt = Text(frame4,height = 1,width = 20,padx=15,pady=15,font=("Constantia", 14))
        inputtxt.grid(row=0,column=0)
        inputtxt.config(state=NORMAL)

        # Function that gets the word entered from the Input TextBox and passes it on to get checked
        def enterWord():
            inputWord = inputtxt.get(1.0,END).strip().upper()
            inputtxt.delete(1.0,END)
            checkIfWordPresent(inputWord)

        # Function that is triggered when user clicks Finish button to end the game manually, and sends EXIT to the Server
        def endGameManual():
            s.send(bytes("EXIT", 'utf-8'))
            endGame()

        # Creating Enter button and assigning command and image to it
        enterImage = PhotoImage(file="images/enter.png")
        enterButton = Button(frame4,image=enterImage, highlightthickness=0,command=enterWord)
        enterButton.img = enterImage
        enterButton.grid(row=0, column=1)

        # Creating Finish button and assigning command and image to it
        endImage = PhotoImage(file="images/end.png")
        endButton = Button(frame4,image=endImage, highlightthickness=0,command=endGameManual)
        endButton.img = endImage
        endButton.grid(row=0, column=2, padx=(15,0))

        # Function to check if entered word is present in the puzzle or not
        def checkIfWordPresent(inputWord):
            # Checks if the word entered by the user has already been entered before and displays a message in frame9 accordingly
            if(inputWord in inputWords):
                message_label.config(text = "You have already entered this word, type a new word!",fg="red")
            else:
                # If entered word is a new word, it is encoded and sent to Server over TCP
                sendWord = bytes(inputWord, 'utf-8')
                s.send(sendWord)
                # Receive a pickled list from Server and unpickle it
                receiveListByte = s.recv(4096)
                receiveList = pickle.loads(receiveListByte)
                # If length of received list is 1, entered word is not present in the puzzle and a message is displayed in frame9 accordingly
                if len(receiveList) == 1:
                    print("Entered word is not present in the sleuth")
                    print(receiveList)
                    message_label.config(text = "Entered word is not present in the sleuth!",fg="red")
                else:
                    # Otherwise, entered word is added to the list of entered words
                    inputWords.append(inputWord)
                    print(receiveList)
                    # Score is incremented
                    global SCORE
                    SCORE+=1
                    # Coordinates of the word are obtained from the received list and are stored in variables
                    row1 = receiveList[0]
                    col1 = receiveList[1]
                    row2 = receiveList[2]
                    col2 = receiveList[3]
                    # Function to highlight the word is called and the coordinates are passed as parameters
                    colorWord(row1,col1,row2,col2)
                    # Function to update the score in scoreboard of frame6 is called
                    updateScore()
                    # Function to update the list of guessed words in frame7 is called and a message is displayed accordingly in frame9
                    updateGuessedWordsFrame()
                    message_label.config(text = "Correct!",fg="green")
                # After updating score, function to check if game is over is called
                checkIfGameOver()

        # Function to highlight a word in the puzzle, receives coordinates as parameters
        def colorWord(row1,col1,row2,col2):
            # If column values are same, it is a vertical word and row values are updated in the for loop
            if(col1==col2):
                for i in range(row1,row2+1):
                    t.color(frame3,i,col1)
            # Else row values are same, it is a horizontal word and column values are updated in the for loop
            else:
                for i in range(col1,col2+1):
                    t.color(frame3,row1,i)

        # Function to update the score in the scoreboard in frame6, configures the label to display latest score
        def updateScore():
            score_img_label.config(text = str(SCORE))

        # Function to update the list of guessed words in frame7, configures the label to display the latest list
        def updateGuessedWordsFrame():
            guessed_words_label.config(text = inputWords)

        # Function to check if the game is over
        def checkIfGameOver():
            # Checks if the score is equal to the word count which means all the words have been guessed, automatically ends the game
            if len(inputWords)==wordCount:
                s.send(bytes("EXIT", 'utf-8'))
                message_label.config(text = "Congratulations! You have found all the words!",fg="green")
                endGame()

        # Function to end the game
        def endGame():
            # Sending list of guessed words as a pickled object over TCP to the Server
            s.send(pickle.dumps(inputWords))
            # Printing final score, list of guessed words and missed words in cmd prompt
            print("\nYour final score: " + str(SCORE))
            print("\n\nWords you guessed:\n")
            print(inputWords)
            print("\n\nWords you missed:\n")
            # Receiving list of missed words from the Server over TCP as a pickled object and unpickling it
            receiveMissedWordsByte = s.recv(4096)
            receiveMissedWords = pickle.loads(receiveMissedWordsByte)
            print(receiveMissedWords)
            # Displaying the list of missed words in frame8
            missed_words_label.config(text = receiveMissedWords)

        print("Enter words from the sleuth, to exit press finish:\n")
        gameWindow.mainloop()

# Creating Start button and assigning command and image to it
startImage = PhotoImage(file="images/playnew.png")
startButton = Button(root,image=startImage, highlightthickness=0,command=openGameWindow)
startButton.config( height = 154, width = 300 )
startButton.img = startImage
startButton.pack(pady=(500,0))
root.mainloop()
