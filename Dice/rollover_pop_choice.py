from random import randrange

def rollover_choice_func( initList ):
    """ Return a function that chooses randomly from the list until all options are gone, then refreshes the list """
    def chooser():
        """ Each time it is called, Pop and return a random choice from the remainder """
        # 0. Rollover if required
        if len( chooser.remnList ) == 0:
            chooser.remnList = chooser.origList[:]
        # 1. Random choice
        remLen = len( chooser.remnList )
        return str( chooser.remnList.pop( randrange( remLen ) ) ).rjust(2)
    chooser.origList = initList[:]
    chooser.remnList = initList[:]    
        
    return chooser

roll20_A = rollover_choice_func( list( range(1,21) ) )
roll20_B = rollover_choice_func( list( range(1,21) ) )

for i in range(31):
    print( [ roll20_A() , roll20_B() ] , end=', ' )
    if (i+1)%7 == 0:
        print()