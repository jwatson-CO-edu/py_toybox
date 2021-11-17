##sierpinski.py
##James Watson, June 2009
##Create a square image file depicting a sierpinski carpet

##The Python Imaging Library uses a Cartesian pixel coordinate system, with (0,0) in the
##upper left corner. Note that the coordinates refer to the implied pixel corners; the centre
##of a pixel addressed as (0, 0) actually lies at (0.5, 0.5)
##Coordinates are usually passed to the library as 2-tuples (x, y). Rectangles are represented
##as 4-tuples, with the upper left corner given first. For example, a rectangle covering all of
##an 800x600 pixel image is written as (0, 0, 800, 600).



import Image # imports the Python Image Library for image file management
import ImageDraw # imports the Python Image Library for drawing operations

def split_square(coords,depth,pen):
    squares = []
    if coords[1][0] - coords[0][0] == coords[1][1] - coords[0][1]:
        span = coords[1][0] - coords[0][0]
        unit = span / 3
        if unit > 1:
           pen.rectangle([(coords[0][0] + unit,coords[0][1]+unit),
                                        (coords[0][0] +2*unit - 1,coords[0][1]+2*unit - 1)],
                                        fill = (255,255,255), outline = (255,255,255))
        else:
             pen.point((coords[0][0] + unit,coords[0][1]+unit), fill = (255,255,255))
        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1): # omit the middle square
                   squares.append([(coords[0][0] + i*unit, coords[0][1] + j*unit),
                                                  (coords[0][0] +(i+1)*unit,coords[0][1] +(j+1)*unit)])
        #print len(squares)
    else:
        print "split_square: coordinates were not square"
    if depth > 1:
       for member in squares:
           split_square(member,depth-1,pen)


if __name__ == "__main__":
    
    ## Set variable EDGE to a power of 3
    EDGE = 3**8
    
    chunk = EDGE
    power = 0
    while chunk > 1 and chunk % 3 == 0:
        power += 1
        chunk = chunk / 3
    
    if chunk % 3 != 0 and chunk > 1:
        print "square dimension was not a power of 3"    

    myFile = Image.new("RGB",(EDGE,EDGE)) # color parameter omitted, therefore filled with black
    
    thePen = ImageDraw.Draw(myFile,"RGB")
    
    split_square([(0,0),(EDGE,EDGE)],power,thePen)
    
    myFile.save("carpet.png","PNG")