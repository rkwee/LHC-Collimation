#!/usr/bin/python

# hHalo
lossesH = [2,31,1177,56]
nprim  = 9934100*64.

#vHalo 
lossesV = [0,48,1238,103]
nprim  += 9942100.*64

losses = [lossesH[i]+lossesV[i] for i in range(len(lossesH))]
print "number of primary protons", nprim
for l in losses: print(l/nprim)
