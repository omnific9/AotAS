Instructions for compiling and running Adventures of the Atomic Submarine:

Step 1: Database
The program runs on a MySQL database. 
Create an empty database and use ./utils/AotAS.sql to restore the basic structure of the database. SQLYog is recommended for this.
Use ./utils/EnrollUser.py to create new users. A user name and a password will be prompted. The actual user ID is the combination of user name and password.
When prompted for condition, type FULL. When prompted for stage of change, type any of the five options. This only concerns the homework the user receives.
Note: the database is named "james" by default, and the enrollment program uses "root/root" as the database credentials. Change these accordingly.

Step 2: Server
The server requires Python 2.7.
Run ./server/src/server.py to start the server.

Step 3: Client
The client source code is in ./client/src/
Compiling and running the source code requires the Ren'Py SDK.
Download the Ren'Py SDK at: http://www.renpy.org/latest.html
Once Ren'Py is installed, create a new project, and copy the content in ./client/src/game to the game folder of the new project.
The program can then be run from inside Ren'Py.
Note: The program connects to the server running on localhost. If the server is running elsewhere, change the address in algorithm.rpy

