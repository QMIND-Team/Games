import Human_Player
import Slow_AI
import Fast_AI

Human_Player.HumanPlayer().playGame()

Fast_AI.FastPlayer().playGame()

Slow_AI.SimplePlayer().playGame()

x = "don't end debugging"

# eventually I should should make sure that when a human user rotates a piec when pushed against the right side the piece never go off the grid
# ^ it simply doesn't rotate as of now, which I think is okay

# I'm not sure how efficiency works in python, so I have done stuff to try to make it use pointers but I don't what Python is actually doing...

