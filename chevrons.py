import random

for i in xrange(100):
    row = ""
    for j in xrange(100):
        row += random.choice( ['\\','/'] )
    print row