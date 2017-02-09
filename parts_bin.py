"""
parts_bin.py
James Watson , 2017 February
A collection of solutions in search of a problem
"""

def bin_points( points , radius ):
    """ Try to bin points into categoies based on clustering into a circle """
    # We do not expect the dominant points to be very close together, so let's use a very course / simple binning method
    cutoff = radius ** 2
    centers = [ points[0] ]
    labels = []
    counts = Counter()
    for pnt in points:
        binned = False
        for label , cntr in enumerate( centers ):
            if vec_dif_sqr( pnt , cntr ) <= cutoff:
                labels.append( label )
                counts[ label ] += 1
                binned = True
                break
        if not binned:
            centers.append( pnt )
            label = len( centers ) - 1
            labels.append( label )
            counts[ label ] += 1
    return centers , labels , counts 