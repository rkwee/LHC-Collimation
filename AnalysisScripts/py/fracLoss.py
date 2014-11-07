#!/usr/bin/python

# hHalo
lossesH = [2,31,1177,56]
nprim  = 993400*64.

#vHalo 
lossesV = [0,48,1238,103]
nprim  += 994200.*64

# # sum
losses = [lossesH[i]+lossesV[i] for i in range(len(lossesH))]

# # old hHalo with maybe some bias
# losses = [2,28,769,46]
# nprim  = 687400.*64

# # TCTOUT

# # vHalo
# lossesV = [6,721,1141,1162]
# nprim   = 14742*50.*64

# lossesH = [21,1221,7085,676]
# nprim   += 17237.*50*64

# # TCTin
lossesH = [7517,1030,13,1443]
nprim  = 993400*64.
lossesV = [333,1719,8,969]
nprim  += 994200.*64


# sum
losses = [lossesH[i]+lossesV[i] for i in range(len(lossesH))]
#losses = lossesV


print "number of primary protons", nprim
for l in losses: print(l, l/nprim)
