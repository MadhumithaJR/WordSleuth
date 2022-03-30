# WordSleuth
A graphic, interactive word search game built in Python.

A Word Sleuth is a puzzle game where the player is shown a matrix of alphabets with words hidden in them. The player has to find all such words and is awarded points accordingly. Often, the words are based on a common theme.

## How This Project Works
In this project, a Word Sleuth game is implemented using TCP with GUI on the client side. Puzzle related data is stored in a JSON file and is read by the server. Data pertaining to any one puzzle is sent across to the client by the server. Upon the matrix being displayed, the player is asked to enter the words into a text box on the Client side, the words are checked by the Server and appropriate actions take place depending on whether the entered word is present in the puzzle or not. The player’s score and the list of words found is updated and shown simultaneously. The player may end the game manually or the game ends automatically when all the words are found.

# Technologies Used
 - Socket programming to establish the connection between the Server (server.py) and the Client (client.py) and transmit all data.
 - The source code is implemented in Python.
 - The data pertaining to the puzzles is stored in a JSON file (data.json).
 - The GUI is implemented on the Client side using Tkinter library in Python.
 - All images displayed in the GUI are stored in a folder titled ‘images’.

# Flow of The Game
![Screenshot (311)](https://user-images.githubusercontent.com/69978576/160856177-e84893d2-9346-468a-aa21-4dd5aa6dbebe.png)

# Snapshots
## Title Window
![Screenshot (83)](https://user-images.githubusercontent.com/69978576/160857665-84f62170-8e5e-4ad2-8753-3ae7610aa7c8.png)


## Server Listening
![Screenshot (90)](https://user-images.githubusercontent.com/69978576/160857754-2dbb4285-b035-48aa-90fd-642aeee20ac8.png)


## Connection Established and gameWindow Opened
![Screenshot (91)](https://user-images.githubusercontent.com/69978576/160857823-13fd4ec2-7177-4ac3-96aa-d53d717d0b6c.png)


## gameWindow with 'Welcome Message'
![Screenshot (84)](https://user-images.githubusercontent.com/69978576/160857920-3ffb1096-8180-4e8b-b103-1f5e4511472b.png)


## Correct Words Being Highlighted
![Screenshot (85)](https://user-images.githubusercontent.com/69978576/160857953-bdb0b83b-1f46-49cb-86ab-7c951aaaecf9.png)


## Incorrect Word Entered
![Screenshot (86)](https://user-images.githubusercontent.com/69978576/160857991-70398f04-8116-4b6c-bc92-208618b9b4de.png)


## Already Entered Word
![Screenshot (89)](https://user-images.githubusercontent.com/69978576/160858699-66105a6a-f05e-492b-bc03-8be710cc8fa8.png)


## Manually Finishing the Game
![Screenshot (87)](https://user-images.githubusercontent.com/69978576/160858817-83fb7c49-9ed9-4fe9-8272-da93623b0d4c.png)


## All Words Found
![Screenshot (88)](https://user-images.githubusercontent.com/69978576/160859049-42180444-7d2c-41fb-ba72-9817e968a3be.png)
