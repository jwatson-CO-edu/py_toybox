exLst = [ 'a', 'b', 'c' ]


def ordered_combos( lst, accumList = None, prefix = None ):
    """ Return all combos of elements in `lst` """
    
    print( lst, (not lst) )
    
    if not lst:
        return []
    
    N = len( lst )
    if accumList is None:
        rtnLst = []
    else:
        rtnLst = accumList
    
    for i, elem in enumerate( lst ):
        
        
        if (prefix is not None) and (len( prefix ) >= N):
            return []
        if prefix is None:
            nuElem = [ elem ]
        elif prefix is not None:
            nuElem = prefix[:]
            nuElem.append( elem )
        
        
        rtnLst.append( nuElem )
        print( lst[i+1:], rtnLst, nuElem )
        if i < N:
            nxtPiece = ordered_combos( lst[i+1:], accumList = rtnLst, prefix = nuElem )
            if nxtPiece is not None:
                rtnLst.extend(
                    nxtPiece
                )
    return rtnLst
        
res = ordered_combos( exLst ) 
print( '\nResult:' )
print( res )