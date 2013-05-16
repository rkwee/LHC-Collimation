#!/usr/bin/python
#
#
# R Kwee, July 2011

import os, math, time
# ------------------------------------------------------------------------------------------------

workpath = '/afs/cern.ch/work/r/rkwee/HiLumi/'
wwwpath  = '/afs/cern.ch/user/r/rkwee/public/www/HiLumi/'

# ------------------------------------------------------------------------------------------------
def mylabel(font):

    mylabel = TLatex()
    mylabel.SetNDC()
    mylabel.SetTextSize(0.05);    
    mylabel.SetTextFont(font)
    mylabel.SetTextColor(1)

    return mylabel

def mean(vec):
    meanVal = 0.
    N = len(vec)
    for n in vec:
        meanVal += n

    if N > 0:
        meanVal /= N
    return meanVal

def stddev(vec):

    meanVal = mean(vec)
    N = len(vec)
    stddev = 0.
    for n in vec:
        stddev += (meanVal - n)**2

    if N > 1.:
        stddev = math.sqrt(stddev/(N-1))

    return stddev

# ------------------------------------------------------------------------------------------------
