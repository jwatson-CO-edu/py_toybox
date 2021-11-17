# factorizer.py
# James Watson, December 2007
# A resource for finding and working with factors and divisors

# -- CHANGE LOG --
# 12-09-07: Prime-finder optimized
# 08-01-08: Added functions for finding divisors (Project Euler Problem # 12)
# 08-07-08: Improved prime number finding algorithm speed (Project Euler Problem # 10)
# 08-07-08: Added function for shortcut prime tests (Project Euler Problem # 35)
# 08-08-08: Added function to test if a given number is prime (Project Euler Problem # 35)
# 08-08-08: Added default values for primeList parameters in case a list was not provided
# 07-14-09: Added and initialized primeList as a variable global to module initialized on load.  This prevents
#generating the same prime numbers multiple times in the same session.  This also eliminates the
#need for the client code to store its own list of primes.  INTERFACE IS NEW AND WILL BREAK OLD CODE
# 07-14-09: Allowed client code access to copy of list of session primes with get_primes()


from math import sqrt, floor

primeList = [2]

def dirty_prime_tricks(number):
    numStr = str(number)
    rejectPrime = False
    # Check for divisibility by 5 by last digit == 5
    if number > 5 and numStr[-1] == "5":
        rejectPrime = True
    else:
        if number > 3:
            # Check for multiple of three by sum of digits%3 == 0
            tally = 0
            for i in numStr:
                tally += int(i)
            if tally%3 == 0:
                rejectPrime = True
    return rejectPrime

def is_prime(number):
    rejectPrime = False
    if not dirty_prime_tricks(number):
        dex = 0
        bound = floor(sqrt(number))
        rejectPrime = False
        while not rejectPrime and dex < len(primeList) and primeList[dex] <= bound:
            if(number%primeList[dex] == 0):
                rejectPrime = True
            else:
                dex += 1
        # Extend, not return, primeList if inadequate to determine primacy of number
        while primeList[-1] <= bound and not rejectPrime:
            primeList = append_next_prime()
            if number%primeList[-1] == 0:
                rejectPrime = True
    else:
        rejectPrime = True
    return not rejectPrime

def append_next_prime():
    primeFound, rejectPrime = False, False
    y = primeList[-1] # Index -1 is the last entry
    while(not primeFound):
        y += 1
        x = 0
    	bound = floor(sqrt(y))
    	rejectPrime = False
    	while not rejectPrime and x < len(primeList) and primeList[x] <= bound:
    	    if(y%primeList[x] == 0):
                rejectPrime = True
    	    else:
    	        x += 1
    	if(not rejectPrime):
    	    primeList.append(y)
    	    #print "Added Prime: " + str(y)
    	    primeFound = True

def factor_branch(chunk, factorList):
    factorFound = False
    factor = 0
    while(not factorFound):
	x = 0
	while(not factorFound and x < len(primeList)):
	    if(chunk%primeList[x] == 0):
		factorFound = True
		chunk = chunk/primeList[x]
		factor = primeList[x]
		#print "Factor: " + str(factor) + " Chunk: " + str(chunk)
	    x += 1
	    if(not factorFound):
		while(not factorFound):
		    append_next_prime()
		    if(chunk%primeList[-1] == 0):
			factorFound = True
			factor = primeList[-1]
			chunk = chunk/primeList[-1]
			#print "Factor: " + str(factor) + " Chunk: " + str(chunk)
	factorList.append(factor)
	if(chunk/factor >= 1):
	    chunk, factorList = factor_branch(chunk, factorList)
    return chunk, factorList

def prime_factors_of(bigNum):
    chunck, factorList = bigNum, [1]
    if(bigNum > 1):
	largestPrime, factorList = factor_branch(chunck, factorList)
    return factorList


def get_combos(numList,size):
    tempCombo1, tempCombo2 = [], []
    #print "in get_combos with size " + str(size)
    if size > 1:
        # Avoid repeated combinations in an ordered factor list
        repChk = -1
        for i in range(0, len(numList)-(size-1)):
            if numList[i] != repChk:
                repChk = numList[i]
                tempCombo2 = get_combos(numList[i+1:],size-1)
                for k in tempCombo2:
                    x = numList[i]*k
                    #print "appending divisor " + str(x)
                    tempCombo1.append(x)
    elif size == 1:
        # size 1 combo lists should not have repeats (no repeated divisors)
        repChk = -1
        for j in range(0, len(numList)):
            if numList[j] != repChk:
                tempCombo1.append(numList[j])
                repChk = numList[j]
    else:
        print "get_combos: INDEX ERROR!"
    return tempCombo1

def strip_repeats(numList):
    # This only works on ordered lists
    repChk, retList = -1, []
    for i in numList:
        if i != repChk:
            retList.append(i)
            repChk = i
    return retList

def rec_divisors(splitNum):
    primeFacts = prime_factors_of(splitNum)
    bigList, bigNum = [], 1
    # use list1.extend(list2) to concatenate list2 to the end of list1
    bigList.extend(strip_repeats(primeFacts))
    for i in range(2,len(primeFacts)):
        divisors = get_combos(primeFacts[1:],i)
        bigList.extend(divisors)
    #bigList.sort() # for testing purposes only, compare to brute_divisors
    return bigList

def brute_divisors(bigNum):
    divisors = []
    for i in range(1,bigNum+1):
	if bigNum % i == 0:
	    divisors.append(i)
    return divisors

def proper_divisors(splitNum):
    # Proper Divisors: numbers less than n which divide evenly into n
    # rec_divisors returns n as part of the list, so trim list
    return rec_divisors(splitNum)[:-1]

def get_primes():
    """Return a COPY of the internal list of primes for this session"""
    # It is inadvisable for the the user to touch this list!
    return primeList[:]