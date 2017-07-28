def add_all( *args ):
    sumA = 0;
    for arg in args:
        sumA += arg
    return sumA

foo = [ 1 , 2 , 3 ]

print add_all( *[ -i for i in foo ] )