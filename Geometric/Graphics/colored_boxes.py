#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
colored_boxes.py , Built on Geany for Python 2.7
James Watson, 2016 June
Possible display for grid-world games
"""

"""
== TODO ==
* Store references to graphics in the graph objects
"""

import Tkinter

topWin = Tkinter.Tk() # Create the root window
topWin.title("Grid World") # title the root window

# Create a drawing canvas attached to root withow with specified BG color and dims
canvas = Tkinter.Canvas(topWin, bg='white', height=300, width=300)

squares = {} # Holds references to square graphics

s = 40 # side of a grid square
pad = 10 # padding b/n rows and cols

for i in range(3): # for each column
	for j in range(3): # for each row
		lft = pad + i * (s + pad) # construct the left of top-left
		top = pad + j * (s + pad) # construct the top  of top-left
		# create a square at this coord and store a reference in the dictionary
		squares[ (i,j) ] = canvas.create_rectangle( lft, top, lft + s, top + s, fill="blue")

canvas.pack() # place the canvas in the window
topWin.mainloop() # start the Tkinter event loop
