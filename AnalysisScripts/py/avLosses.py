#!/usr/bin/python
#
#
# Oct 2014, rkwee
# -------------------------------------------------------------------------------
import ROOT, sys, glob, os, time, math
from ROOT import *
import lossmap, helpers, array
from helpers import wwwpath, file_len, length_LHC, mylabel, addCol, gitpath, workpath
# -------------------------------------------------------------------------------

def avLosses(rfname, coll, scaleFactor, hname, loss_start, loss_end, pointName):

	debug = 1

        trname = 'normtree' + coll

        print "Calculating losses from ", hname, " in ",pointName, " from ", loss_start, " to ", loss_end

        rf = TFile.Open(rfname)
        nt = rf.Get(trname)

	norm = -9999
	for entry in nt: 
		norm = getattr(entry,coll)
		if debug: print 'norm', norm

	hist = rf.Get(hname)
	if int(norm):  hist.Scale(1./norm)
	else: "rootfile OK? Got zero norm."

        max_losses, losses = [],[]

        # norm = 1.
        bin_start = hist.FindBin(loss_start)
        bin_end   = hist.FindBin(loss_end)
        avloss    = hist.Integral(bin_start,bin_end)
        nbins     = bin_end - bin_start

	sum_cont = 0
	cluster1, cluster2, ibins = [],[],[]
	for i in range(nbins+1):
            ibin = bin_start + i
	    cont = hist.GetBinContent(ibin)

	    if pointName.count("cluster 1"): cluster1 += [cont]
	    elif pointName.count("cluster 2"): cluster2 += [cont]

	    ibins    += [ibin]
	    if cont :
		    #print "bincontent", cont, 'ibin', ibin
		    sum_cont += cont

	print "Intgral losses", avloss
	print "summed losses", sum_cont

	if pointName.count("cluster 1"): 
		maxlossCl1 = max(cluster1)
		idxCl1 = cluster1.index(maxlossCl1)

	if pointName.count("cluster 2"): 
		maxlossCl2 = max(cluster2)
		idxCl2 = cluster2.index(maxlossCl2)

	if pointName.count("cluster 1"): print "maxloss", maxlossCl1, 'in bin', ibins[idxCl1], ' of ', pointName
	if pointName.count("cluster 2"): print "maxloss", maxlossCl2, 'in bin', ibins[idxCl2], ' of ', pointName

        # statistical uncertainty
        stat = 0.

        if debug:
            print('averaging over ',nbins,' bins, from bin ' + str(bin_start) + ' to bin ' + str(bin_end))

        max_loss = hist.GetMaximum()/scaleFactor

	print "max_loss in cold histogram", max_loss
	# structure: simulation case, loss in bin range, statistical error, maximal loss in bin range, its statistical error
        losses  += [ sum_cont, avloss/nbins, math.sqrt(avloss)/nbins, max_loss, math.sqrt(max_loss) ]
        
	if debug: 
		print "simulation case, loss in bin range, statistical error, maximal loss in bin range, its statistical error ", losses

		# maximum loss not necessary in the selected bin range
		print "Maximum loss",hist.GetMaximum()," in bin", hist.GetMaximumBin(), \
			    " from ", hist.GetBinLowEdge(hist.GetMaximumBin()), " to ", hist.GetBinLowEdge(hist.GetMaximumBin() + 1)

	return losses
