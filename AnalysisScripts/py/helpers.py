#!/usr/bin/python
#
#
# R Kwee, June 2013

import os, math, time, ROOT
from ROOT import TLatex
import gzip
# ------------------------------------------------------------------------------------------------

workpath = '/afs/cern.ch/work/r/rkwee/HL-LHC/'
wwwpath  = '/afs/cern.ch/user/r/rkwee/public/www/HL-LHC/'
source_dir  = workpath + 'runs/sourcedirs/'
gitpath  = workpath + 'HL-LHC-Collimation/AnalysisScripts/'
# ------------------------------------------------------------------------------------------------
length_LHC = 26659
IPs = [
 ("IP1",        0.000000  ),      
 ("IP2",     3332.436584  ),      
 ("IP3",     6664.720800  ),      
 ("IP4",     9997.005016  ),      
 ("IP5",    13329.289233  ),      
 ("IP6",    16661.725816  ),      
 ("IP7",    19994.162400  ),      
 ("IP8",    23315.378983  ),      
]

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
# first two numbers correspond to warm sections (ie element 0 and 1) if value is inbetween second and third number (ie between element 1 and 2 of the list) it's considered to be in a cold sector)

warm = [0.0,22.5365,54.853,152.489,172.1655,192.39999999999998,199.48469999999998,224.3,3095.454284,3155.628584,3167.740084,3188.4330840000002,3211.4445840000003,3263.867584,3309.9000840000003,3354.9740840000004,3401.005584,3453.4285840000002,3476.440084,3494.065584,3505.885284,3568.318584,6405.4088,6457.9138,6468.7785,6859.513800000001,6870.3785,6923.5338,9735.907016000001,9824.730516000001,9830.832016,9861.730516,9878.732016,9939.985516,9950.548016,10043.462016,10054.024516,10115.278016,10132.279516,10163.970516,10170.072016,10257.603016,13104.989233,13129.804533,13136.889233,13157.123733,13176.800233,13271.647233,13306.752733,13351.825733,13386.931233000001,13481.778233000001,13501.454732999999,13522.784533,13529.869233,13554.684533,16394.637816,16450.871316,16456.972816,16487.271316000002,16493.372816,16830.871316,16836.972815999998,16867.271316,16873.372816,16928.294816,19734.8504,19760.6997,19771.5644,20217.9087,20228.773400000002,20252.9744,23089.979683999998,23138.576984,23150.396684,23171.375484,23194.386984,23246.809984,23292.842484,23337.915484,23383.947984,23436.370984,23459.382483999998,23480.082484,23492.193984,23553.115984,26433.4879,26458.3032,26465.387899999998,26486.7177,26506.3942,26601.2412,26636.346700000002,26658.883199999997]

def addCol(fileName, colNumber):

    n = 0
    with open(fileName) as mf:
        for line in mf:

            try:
                n += float(line.split()[colNumber])

            except ValueError:    
                pass

    return n


def file_len(fname):

    if fname.endswith('gz'):
        i = 0
        f = gzip.open(fname,'r')
        for line in f:
           i += 1
        return i
    else:
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

def sum_npart(fname,index):
    # fname = file 
    # index = colum number that indicates particle number
    # all header strings are skipped 

    npart = []
    with open(fname) as f:
        for line in f:

            try:
                ipart = float(line.split()[index]) 
                
                if ipart not in npart:
                    npart += [ipart]

            except ValueError:
                pass
    return sum(npart)


def count_npart(fname,index):
    # fname = file 
    # index = colum number that indicates particle number
    npart = []
    with open(fname) as f:
        for line in f:
            try:
                ipart = float(line.split()[index]) 
                if ipart not in npart:
                    npart += [float(ipart)]
            except ValueError:
                pass

    return len(npart)


def rename(fullpattern, suppresspattern):

    # remove suppresspattern from fullpattern

    return fullpattern.split(suppresspattern)[0]+ fullpattern.split(suppresspattern)[-1]
    

