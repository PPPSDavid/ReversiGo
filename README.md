# The reversi game 

This is a project that implements the different aspects of board game Reversi, 
including one basic board to display current game and an I/O using pair of numbers
as location and +-1 as color. 

This game also includes several artificial intellegence methods to play with, including 
the one based on memory-intenside iteration min-max search tree, the recursion 
version of min-max search tree and the one using a simple alpha-beta search tree.Besides that 
is the approach using neural network as a "value" judging system and MTCR search tree.

It is still INPROGRESS! I am relative new on Python, so the code is a bit ugly(ik) but I will be fixing that. 

The current playable part is the UI.py file. It enables a match between users and users or computers. Selfplay.py files are for
testing including multi-threading, so they are not a playable part.

The main file is GameCore.py, most part of the AI is implemented there.
