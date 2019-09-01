# chevrons.py
# Print some random, angular glyphs

# TODO: Make the dicerolls tunable

import random

seq = [ 
    [ '\\' , '/' ] ,
    [ '\\' , '/' , '-' , '|' , '_' , ' ' , ' ' ] ,
    [ '\\' , '/' , ' ' ] ,
    [ '\\' , '/' , '_' ] ,
]

for i in range( 100 ):
    row = ""
    for j in range( 100 ):
        row += random.choice( seq[3] )
    print( row )
