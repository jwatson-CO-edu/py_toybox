# chevrons.py
# Print some random, angular glyphs

# TODO: Make the dicerolls tunable

import random

for i in xrange(100):
    row = ""
    for j in xrange(100):
        row += random.choice( ['\\','/','-','|','_',' ',' '] )
    print row