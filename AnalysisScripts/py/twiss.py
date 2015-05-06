#!/usr/bin/python
#
# Mar 201, rkwee
## -------------------------------------------------------------------------------
import pymadx
# -----------------------------------------------------------------------------------
def compare():

    # twiss file
    v10tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/HL_TCT_7TeV/twiss.hllhcv1.b1.tfs')
    v11tf = pymadx.Tfs('/afs/cern.ch/work/r/rkwee/HL-LHC/runs/sourcedirs/HL_TCT_7TeV/twiss.hllhcv1.1-b1.tfs')


    v10BetX = v10tf.GetColumnDict('BETX')
    v10BetY = v10tf.GetColumnDict('BETY')
    v10AlfX = v10tf.GetColumnDict('ALFX')
    v10AlfY = v10tf.GetColumnDict('ALFY')
    v10X    = v10tf.GetColumnDict('X')
    v10Y    = v10tf.GetColumnDict('Y')
    v10S    = v10tf.GetColumnDict('S')
    v10PX   = v10tf.GetColumnDict('PX')
    v10PY   = v10tf.GetColumnDict('PY')

    v10colls = ['TCTH.4L1.B1', 
                'TCTVA.4L1.B1', 
                'TCTH.5L1.B1', 
                'TCTVA.5L1.B1', 

                'TCTH.4L5.B1', 
                'TCTVA.4L5.B1', 
                'TCTH.5L5.B1', 
                'TCTVA.5L5.B1', 
                ]

    print "NAME S BETX BETY SIGX SIGY in v1.0" 
    for coll in v10colls:

        betX = v10BetX[coll]
        betY = v10BetY[coll]
        alfX = v10AlfX[coll]
        alfY = v10AlfY[coll]
        x,y,s  = v10X[coll], v10Y[coll], v10S[coll]
        pX, pY = v10PX[coll], v10PY[coll]

        #print "alfX, x, pX, y, pY",  alfX, x, pX, y, pY
        # values
        gamX = 1./betX*(1.+alfX**2)
        gamY = 1./betY*(1.+alfY**2)

        emiX = gamX*x**2 + 2.*alfX*x*pX + betX* pX**2
        emiY = gamY*y**2 + 2.*alfY*y*pY + betY* pY**2

        sigX = betX * emiX
        sigY = betY * emiY

        print coll,' ', s, betX, betY, sigX, sigY

    print '-'*30
    
    v11BetX = v11tf.GetColumnDict('BETX')
    v11BetY = v11tf.GetColumnDict('BETY')
    v11AlfX = v11tf.GetColumnDict('ALFX')
    v11AlfY = v11tf.GetColumnDict('ALFY')
    v11X    = v11tf.GetColumnDict('X')
    v11Y    = v11tf.GetColumnDict('Y')
    v11PX   = v11tf.GetColumnDict('PX')
    v11PY   = v11tf.GetColumnDict('PY')
    v11S    = v11tf.GetColumnDict('S')

    v11colls = ['TCTH.4L1.B1', 
                'TCTV.4L1.B1', 
                'TCTH.5L1.B1', 
                'TCTV.5L1.B1', 

                'TCTH.4L5.B1', 
                'TCTV.4L5.B1', 
                'TCTH.5L5.B1', 
                'TCTV.5L5.B1', 
                ]
 
    print "NAME S BETX BETY SIGX SIGY in v1.1" 
    for coll in v11colls:

        betX = v11BetX[coll]
        betY = v11BetY[coll]
        alfX = v11AlfX[coll]
        alfY = v11AlfY[coll]
        x,y,s  = v11X[coll], v11Y[coll], v11S[coll]
        pX, pY = v11PX[coll], v11PY[coll]


        # values
        gamX = 1./betX*(1.+alfX**2)
        gamY = 1./betY*(1.+alfY**2)

        emiX = gamX*x**2 + 2.*alfX*x*pX + betX* pX**2
        emiY = gamY*y**2 + 2.*alfY*y*pY + betY* pY**2

        sigX = betX * emiX
        sigY = betY * emiY

        print coll,' ', s, betX, betY, sigX, sigY

# ----------------------------------------------------------------------------
if __name__ == "__main__":

    compare()

