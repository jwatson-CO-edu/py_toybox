##squareDraw.py
##James Watson, July 2009
##A program to draw a matrix of random patterns onto squares for icons, avatars, and other generally
##useless applications
## Requires Python Image Library
## Requires factorizer module (James Watson)
## Assumes rectangle coordinates of the form [(x1,y1),(x2,y2)]
## Convention: if a parameter is not specified, it is randomly set within possible range

## -- TO DO --
## * Some orientations can be eliminated by specifying foreground and background colors



import Image # imports the Python Image Library for image file management
import ImageDraw # imports the Python Image Library for drawing operations
import factorizer # James Watson module for prime and proper factors
import random


def grid_divide(coords, size = None):
    """divides a rectangle into a regular grid of squares, return None otherwise"""
    squares = []
    xLen = coords[1][0] - coords[0][0]
    yLen = coords[1][1] - coords[0][1]
    xDiv = factorizer.rec_divisors(xLen)[1:]
    yDiv = factorizer.rec_divisors(yLen)[1:]
    if len(xDiv) == 1 and len(yDiv) == 1:
        print "grid_divide: dimensions were prime, even divisions > 1px not possible"
    else:
        common = []
        for n in xDiv:
            if n in yDiv:
                common.append(n)
        unit = 0
        if len(common) > 0:
            unit = random.choice(common)
            if size in common:
                unit = size
            else:
                print "grid_divide: requested division size is not available"
            for i in range(xLen / unit):
                for j in range(yLen / unit):
                    squares.append([(coords[0][0] + i*unit, coords[0][1] + j*unit),
                                    (coords[0][0] +(i+1)*unit - 1,coords[0][1] +(j+1)*unit-1)])
        else:
            print "grid_divide: could not negotiate square divisions"
    if len(squares) == 0:
        squares = None
    return squares

def sqr_fill(coords, pen, fillCol = None):
    """Fill the square with a single color"""
    if not fillCol:
        fillCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    pen.rectangle(coords,fill = fillCol,outline = fillCol)

def sqr_diag(coords, pen, orient = None, fillCol = None, bgCol = None):
    """Split the square diagonally into to two colored regions"""
    # Left-Hand (LH) orientation is from upper left to lower right
    # Right-Hand (RH) orientation is from upper right to lower left
    xLen = coords[1][0] - coords[0][0]
    yLen = coords[1][1] - coords[0][1]
    if not fillCol:
        fillCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    if not bgCol:
        bgCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    if not orient:
        orient = random.choice(["LH","RH"])
    if orient == "LH":
        pen.rectangle(coords, fill = bgCol, outline = bgCol)
        pen.polygon([(coords[0][0],coords[0][1]),(coords[1][0],coords[1][1]),
                     (coords[0][0] , coords[1][1])], fill = fillCol, outline = fillCol)

    elif orient == "RH":
        pen.rectangle(coords, fill = bgCol, outline = bgCol)
        pen.polygon([(coords[1][0],coords[0][1]),(coords[0][0],coords[1][1]),
                     (coords[1][0], coords[1][1])],
                    fill = fillCol, outline = fillCol)
    else:
        print "sqr_diag: orient must either be 'LH' or 'RH'"

def sqr_rhom(coords, pen, orient = None, fillCol = None, bgCol = None):
    """Draw a rotated square with corners touching the mid-points of bounding square's edges"""
    xLen = coords[1][0] - coords[0][0]
    yLen = coords[1][1] - coords[0][1]
    if not fillCol:
        fillCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    if not bgCol:
        bgCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    pen.rectangle(coords, fill = bgCol, outline = bgCol)
    pen.polygon([(coords[0][0] + round(xLen/2.0),coords[0][1]),
                 (coords[0][0],coords[1][1] - round(yLen/2.0)),
                 (coords[1][0] - round(xLen/2.0),coords[1][1]),
                 (coords[1][0],coords[0][1] + round(yLen/2.0))], fill = fillCol, outline = fillCol)

def dec_to_str_bin(num, formLen = 8):
    if num < 0:
        raise ValueError, "Must be a positive integer"
    rtnStr = ""
    if num == 0:
        rtnStr = '0'
    else:
        try:
            rtnStr = bin(num) # binary conversion function new to Python 2.6
        except(NameError):
            #if not BINWARN:
                print "Function bin() not available in this version of Python"
                #BINWARN = True
        if len(rtnStr) < 1: # builtin bin() failed, use our function
            rem = num
            while rem > 0:
                rtnStr = str(rem % 2) + rtnStr
                rem = rem >> 1 # bitwise shift left 1 place (divide by 2)
    while len(rtnStr) < formLen:
        rtnStr = "0" + rtnStr
    return rtnStr

#def sqr_auto(coords,pen,size = None,fillCol = None, bgCol = None, wolfCode = None, orient = None, seedSpace = 3):
    #""" Draws a 1-dimensional cellular automaton, defined by specifified Wolfram Code """
    #xLen = coords[1][0] - coords[0][0]
    #yLen = coords[1][1] - coords[0][1]
    #if not wolfCode:
        #wolfCode = random.randrange(256)
    #elif wolfCode < 0 or wolfCode > 255:
        #print "sqr_auto: Wolfram Code was not in range 0 - 255"
    #wolfCode = dec_to_str_bin(wolfCode)
    #wolfKey = {}
    #if len(wolfCode) == 8:
        #state = 0
        #for char in wolfCode:
            #key = dec_to_str_bin(state, formLen = 3)
            #if char == '1':
                #wolfKey[key] = 1
            #elif char == '0':
                #wolfKey[key] = 0
            #else:
                #print "sqr_auto: encountered invalid character " + char
    #else:
        #print "sqr_auto: Wolfram Code was of incorrect length"
    #if not orient:
        #orient = random.choice(['N','E','S','W'])
    #if not fillCol:
        #fillCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    #if not bgCol:
        #bgCol = (random.randrange(256),random.randrange(256),random.randrange(256))
    #lastGen = []
    #if orient == 'N':
        #for i in range(xLen + 1):
            #if not random.randrange(seedSpace): # There are 1 to seedSpace odds of returning True
                #pen.point((coords[0][0] + i, coords[0][1]), fill = fillCol)
                #lastGen.append(1)
            #else:
                #pen.point((coords[0][0] + i, coords[0][1]), fill = bgCol)
                #lastGen.append(0)
        #for j in range(1, yLen + 1):
            #for k in range(xLen + 1)
    #elif orient == 'E':
        #pass
    #elif orient == 'S':
        #pass
    #elif orient == 'W':
        #pass
    #else:
        #print "sqr_auto: orient must be equal to 'N', 'E', 'S', or 'W'"

if __name__ == "__main__":

    EDGE = 200
    
    BINWARN = False # Flag for Python version of binary conversion warning.
    
    myFile = Image.new("RGB",(EDGE,EDGE), color = (255,255,255))
    thePen = ImageDraw.Draw(myFile,"RGB")
    
    regions = grid_divide([(0,0),(EDGE,EDGE)], size = 40)
    
    funcs = []
    funcs.append(sqr_fill)
    funcs.append(sqr_diag)
    funcs.append(sqr_rhom)
    
    for k in regions:
        random.choice(funcs)(k,thePen) # randomly choose one of the drawing functions above
    
    ##for k in regions:
    ##    sqr_fill(k,thePen)
    
    myFile.save("randSquares.png","png")