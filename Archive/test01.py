# -*- coding: utf-8 -*-
"""
FILENAME.py , Built on Spyder for Python 2.7
James Watson, YYYY MONTHNAME
A ONE LINE DESCRIPTION OF THE FILE

"""

# Standard Libraries
import math
from math import sqrt, ceil
# Special Libraries
import matplotlib.pyplot as plt
import numpy as np
# == Constants ==
EPSILON = 1e-7

# == Helper Functions ==

def eq(op1, op2):
    """ Return true if op1 and op2 are close enough """
    return abs(op1 - op2) <= EPSILON

# == End Helper ==

import sys
print sys.path