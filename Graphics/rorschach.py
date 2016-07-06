##rorschach.py
##James Watson, July 2009
##An application to create abstract symmetrical patterns

import Image # imports the Python Image Library for image file management
import ImageDraw # imports the Python Image Library for drawing operations
import random

EDGE = 300

myFile = Image.new("RGB",(EDGE,EDGE), color = (255,255,255))
thePen = ImageDraw.Draw(myFile,"RGB")

myFile.save("randSquares.bmp","BMP")