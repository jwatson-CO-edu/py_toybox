exLst = [ 'a', 'b', 'c' ]


def ordered_combos( lst, accumList = None, prefix = None, maxLen = None ):
    """ Return all combos of elements in `lst` """
    
    N = len( lst )
    d = len( prefix ) if (prefix is not None) else 0

    if (maxLen is None) and (prefix is None):
        maxLen = N
    
    if not lst:
        return []

    if accumList is None:
        rtnLst = []
    else:
        rtnLst = accumList
    
    for i, elem in enumerate( lst ):
        
        if (prefix is not None) and (len( prefix ) >= maxLen):
            return []
        if prefix is None:
            nuElem = [ elem ]
        elif prefix is not None:
            nuElem = prefix[:]
            nuElem.append( elem )
        
        # print( '\t'*d, f"Adding: {nuElem}" )
        
        rtnLst.append( nuElem )
        # print( lst[i+1:], rtnLst, nuElem )
        if i < N:
            ordered_combos( lst[i+1:], accumList = rtnLst, prefix = nuElem, maxLen = maxLen )
    return rtnLst
        
res = ordered_combos( exLst ) 
print( '\nResult:' )
print( res )