import math
from helpers import getBeam, tag_BH_4TeV, tag_BH_7TeV, tag_BH_6p5TeV, tag_BG_4TeV, tag_BH_3p5TeV, tag_BG_6p5TeV, tag_crab_HL, tag_BG_3p5TeV
tag_HL   = 'HL_BH'


# ---------------------------------------------------------------------------------
# dict for histograms, ALL hDicts must have the same structure!!
# ---------------------------------------------------------------------------------
hDict_HL_comp = {

    # ---------------------------------------------------------------------------------
    # comp plots
    # ---------------------------------------------------------------------------------
    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax

    'EkinMuComp' : [['EkinMuBGst', 'EkinMuBGac', 'EkinMuBHds', 'EkinMuBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, '#mu^{#pm}', 0.55,0.85, -1,-1, ],
    'EkinPrComp' : [['EkinPrBGst', 'EkinPrBGac', 'EkinPrBHds', 'EkinPrBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, 'p', 0.55,0.85, -1,-1, ],
    'EkinPhComp' : [['EkinPhBGst', 'EkinPhBGac', 'EkinPhBHds', 'EkinPhBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, '#gamma', 0.55,0.85, -1,-1, ],
    'EkinEpComp' : [['EkinEpBGst', 'EkinEpBGac', 'EkinEpBHds', 'EkinEpBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, 'e^{#pm}', 0.55,0.85, -1,-1, ],
    'EkinNeComp' : [['EkinNeBGst', 'EkinNeBGac', 'EkinNeBHds', 'EkinNeBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, 'n', 0.55,0.85, -1,-1, ],
    'EkinChComp' : [['EkinChBGst', 'EkinChBGac', 'EkinChBHds', 'EkinChBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, '#pi^{#pm}, K^{#pm}', 0.55,0.85, -1,-1, ],

    'RadNMuComp' : [['RadNMuBGst', 'RadNMuBGac', 'RadNMuBHds', 'RadNMuBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, '#mu^{#pm}', 0.55,0.85, -1,-1, ],
    'RadNPrComp' : [['RadNPrBGst', 'RadNPrBGac', 'RadNPrBHds', 'RadNPrBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, 'p', 0.55,0.85, -1,-1, ],
    'RadNPhComp' : [['RadNPhBGst', 'RadNPhBGac', 'RadNPhBHds', 'RadNPhBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, '#gamma', 0.55,0.85, -1,-1, ],
    'RadNEpComp' : [['RadNEpBGst', 'RadNEpBGac', 'RadNEpBHds', 'RadNEpBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, 'e^{#pm}', 0.55,0.85, -1,-1, ],
    'RadNNeComp' : [['RadNNeBGst', 'RadNNeBGac', 'RadNNeBHds', 'RadNNeBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, 'n', 0.55,0.85, -1,-1, ],
    'RadNChComp' : [['RadNChBGst', 'RadNChBGac', 'RadNChBHds', 'RadNChBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, '#pi^{#pm}, K^{#pm}', 0.55,0.85, -1,-1, ],

    'RadEnMuComp' : [['RadEnMuBGst', 'RadEnMuBGac', 'RadEnMuBHds', 'RadEnMuBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, '#mu^{#pm}', 0.55,0.85, -1,-1, ],
    'RadEnPrComp' : [['RadEnPrBGst', 'RadEnPrBGac', 'RadEnPrBHds', 'RadEnPrBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, 'p', 0.55,0.85, -1,-1, ],
    'RadEnPhComp' : [['RadEnPhBGst', 'RadEnPhBGac', 'RadEnPhBHds', 'RadEnPhBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, '#gamma', 0.55,0.85, -1,-1, ],
    'RadEnEpComp' : [['RadEnEpBGst', 'RadEnEpBGac', 'RadEnEpBHds', 'RadEnEpBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, 'e^{#pm}', 0.55,0.85, -1,-1, ],
    'RadEnNeComp' : [['RadEnNeBGst', 'RadEnNeBGac', 'RadEnNeBHds', 'RadEnNeBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, 'n', 0.55,0.85, -1,-1, ],
    'RadEnChComp' : [['RadEnChBGst', 'RadEnChBGac', 'RadEnChBHds', 'RadEnChBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, '#pi^{#pm}, K^{#pm}', 0.55,0.85, -1,-1, ],

}
# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'beamhalo'
tag_HL= '_BH'
hDict_HL_BH = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    # 'Ekin_debug_TCT' : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'], 0.72,0.7,0.98,0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.7, ],
    # 'RadNChar_debug_TCT': [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-6,1, 0, lText, 0.2,0.7, ],

    'Ekin' + tag_HL : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, -1,-1, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9, -1,-1, ],
    'EkinChar' + tag_HL : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinBp' + tag_HL : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinPiInBp' + tag_HL : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNDist' + tag_HL: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,1200,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadNChar' + tag_HL: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-5,2, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNMuons' + tag_HL: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE500'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-8,1e-4, 1, lText, 0.2,0.9, -1,-1, ],
    'RadEnChar' + tag_HL: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-10,1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadEnDist' + tag_HL:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0,1200,1e-10,1, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNDist' + tag_HL: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, 3.14,3.01,1e-3,9, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnChar' + tag_HL: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-2,1e2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNMu' + tag_HL: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -3.14,3.,1e-5,9-1, 1, lText, 0.2,0.9, -1,-1, ],
    'PhiNMuPM' + tag_HL: [ ['PhiNMuons','PhiNMuPlus','PhiNMuMinus'],0.4, 0.64, 0.7, 0.92, 0,1, -3.14,3.,1e-5,9-1, 1, lText, 0.2,0.9, -1,-1, ], 
    'PhiEnMu' + tag_HL: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.2, 0.8, 0.5, 1.0, 0,1, -3.14,3.,1e-5,9-1, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnDist' + tag_HL:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 3.14,3.01,5e-3,5e2, 0, lText, 0.2,0.9, -1,-1, ],

    'PhiEnMuE' + tag_HL:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnMuE100'],0.6, 0.72, 0.9,0.92, 0,1, 3.14,3.01,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt' + tag_HL: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200','PhiEnMuRlt500','PhiEnMuRlt1000'],0.6, 0.72, 0.9,0.92, 0,1, 3.14,3.01,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt200' + tag_HL: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200'],0.6, 0.72, 0.9,0.92, 0,1, 3.14,3.01,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],

    'XcoorNChar' + tag_HL: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e1, 0, lText, 0.2,0.9, -1,-1, ],
    'YcoorNChar' + tag_HL: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e1, 0, lText, 0.2,0.9, -1,-1, ],

    'XYNAll' + tag_HL           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuons' + tag_HL         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNPhotons' + tag_HL       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNElecPosi' + tag_HL      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'XYNNeutronsE' + tag_HL      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNProtonsE' + tag_HL       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNPiPlusE' + tag_HL        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],       
    'XYNPiMinusE' + tag_HL       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNKaonPlusE' + tag_HL      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNKaonMinusE' + tag_HL     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    }
# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'BG a.c.'
tag_HL = '_BGac'
hDict_HL_BGac = { # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax

    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag_HL : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72,0.7,0.98,0.9, 1,1, 2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, -1,-1, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1,  2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, -1,-1, ],
    'EkinChar' + tag_HL : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.6,0.7,0.98,0.9, 1,1, 2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, -1,-1, ],
    'EkinBp' + tag_HL : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6,0.98,0.9, 1,1, 2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, -1,-1, ],
    'EkinPiInBp' + tag_HL : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6,0.98,0.9, 1,1, 2e-2,1e4, 2e2,1e8, 0, lText, 0.7,0.9, -1,-1, ],

    'RadNDist' + tag_HL: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,600,1e-5,1e5, 0, lText, 0.7,0.9, -1,-1, ],
    'RadNChar' + tag_HL: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,1e-5,1e5, 0, lText, 0.7,0.9, -1,-1, ],

    'RadNMuons' + tag_HL: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE1000'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.7,0.9, -1,-1, ],
    'RadEnChar' + tag_HL: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,1e-5,1e9, 0, lText, 0.7,0.9, -1,-1, ],
    'RadEnDist' + tag_HL:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0.,600,1e-5,1e9, 0, lText, 0.7,0.9, -1,-1, ],
    'PhiNDist' + tag_HL: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, 3.14,3.01,1e3,1e8, 0, lText, 0.3,0.9, -1,-1, ],
    'PhiEnChar' + tag_HL: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52,0.75,0.98,0.9, 0,1, 3.14,3.01,1e5,2e10, 0, lText, 0.5,0.9, -1,-1, ],
    'PhiNMu' + tag_HL: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4,0.64,0.7,0.92, 0,1, 3.14,3.01,1e2,1e5, 0, lText, 0.7,0.9, -1,-1, ], 
    'PhiEnMu' + tag_HL: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.2, 0.7, 0.5, 1.0, 0,1, 3.14,3.01,1e1,1e8, 1, lText, 0.7,0.9, -1,-1, ],
    'PhiEnDist' + tag_HL:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 3.14,3.01,1e3,2e10, 0, lText, 0.3,0.9, -1,-1, ],

    'XcoorNChar' + tag_HL: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-2,1e7, 0, lText, 0.7,0.9, -1,-1, ],
    'YcoorNChar' + tag_HL: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-2,1e7, 0, lText, 0.7,0.9, -1,-1, ],

    'XYNAll' + tag_HL           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNMuons' + tag_HL         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNPhotons' + tag_HL       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNElecPosi' + tag_HL      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],

    'XYNNeutronsE' + tag_HL      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNProtonsE' + tag_HL       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNPiPlusE' + tag_HL        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],       
    'XYNPiMinusE' + tag_HL       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNKaonPlusE' + tag_HL      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],
    'XYNKaonMinusE' + tag_HL     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, -1,-1, ],

    }

# --------------------------------------------------------------------------------------------------------------------------------------------------------

#lText = 'offmom +500Hz 6.5 TeV'


scaleFactor = 1.
if tag_BH_4TeV.count('20GeV'): scaleFactor = 0.1

tag = tag_BH_4TeV
Beam, beam, beamn = getBeam(tag)
# lText = 'offmom -500Hz 4 TeV'
# lText = 'offmom +500Hz 4 TeV'
lText = 'beamhalo 4 TeV ' + Beam


# tag = tag_BH_3p5TeV
# Beam, beam, beamn = getBeam(tag)
# lText = ' beamhalo 3.5 TeV ' + Beam

hDict_BH_4TeV = { 


    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, -1,-1, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9, -1,-1, ],
    'EkinChar' + tag : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinBp' + tag : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinPiInBp' + tag : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,600,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE500'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.9, -1,-1, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0,600,1e-9,2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, 3.14,3.01,1e-5,1e1, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, 3.14,3.01,1e-5,1, 1, lText, 0.2,0.9, -1,-1, ], 
    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 3.14,3.01,1e-3,1e2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-3,1e2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.6, 0.6, 0.9,0.9, 0,1, 3.14,3.01,1e-5,1e3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuRlt' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200','PhiEnMuRlt300','PhiEnMuRlt400','PhiEnMuRlt500','PhiEnMuRlt1000'],0.6, 0.6, 0.9,0.9, 0,1, 3.14,3.01,1e-5,1e3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnCharRlt' + tag: [ ['PhiEnCharRlt10','PhiEnCharRlt100','PhiEnCharRlt200'],0.6, 0.6, 0.9,0.9, 0,1, 3.14,3.01,1e-5,1e3, 0, lText, 0.2,0.9, -1,-1, ],

    'XcoorNChar' + tag: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, -1,-1, ],
    'YcoorNChar' + tag: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, -1,-1, ],

    'XYNAll' + tag         : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 1,0, -30,30,-30,30, 0, lText, 0.2,0.9, 1e-7,1e-2, ],
    'XYNMuons' + tag       : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 1e-6*scaleFactor,2e-5*scaleFactor, ],
    'XYNMuonsE10' + tag    : [ ['XYNMuonsE10'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 1e-6*scaleFactor,2e-5*scaleFactor, ],
    'XYNMuonsE500' + tag    : [ ['XYNMuonsE500'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 1e-6*scaleFactor,2e-5*scaleFactor, ],
    'XYNPhotons' + tag     : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 8e-6,2e-3, ],
    'XYNPhotonsZoom' + tag  : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 1,0, -15,15,-15,15, 0, lText, 0.2,0.9, 8e-6,2e-3, ],
    'XYNElecPosi' + tag    : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 1e-8,3e-6, ],
    'XYNChar' + tag        : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, -100,100,-100,100, 0, lText, 0.2,0.9, 2e-7,5e-3, ],
    'XYNCharZoom' + tag    : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, -15,15,-15.,15., 0, lText, 0.2,0.9, 2e-7,5e-3, ],

    'XYNProtons' + tag       : [ ['XYNProtons'], 0.5, 0.88, 0.83, 0.92, 1, 0, -30, 30, -30, 30, 0, lText, 0.2,0.96, 6e-7,1e-4, ],
    'XYNProtonsE10' + tag   : [ ['XYNProtonsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 1e-7,1e-5, ],
    'XYNProtonsE100' + tag   : [ ['XYNProtonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 1e-7,1e-5, ],
    'XYNProtonsE500' + tag   : [ ['XYNProtonsE500'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 1e-7,1e-4, ],

    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.75, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsZoom' + tag    : [ ['XYNPhotons'], 0.75, 0.88, 0.83, 0.92, 1,0, -15,15,-15,15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsE10' + tag     : [ ['XYNPhotonsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsE100' + tag    : [ ['XYNPhotonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNNeutrons' + tag       : [ ['XYNNeutrons'], 0.75, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNNeutronsE10' + tag     : [ ['XYNNeutronsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNNeutronsE100' + tag    : [ ['XYNNeutronsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    
    'XYNNeutronsE' + tag   : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 1,0, -50,50,-1,-1, 0, lText, 0.2,0.96, 1e-8,1e-4, ],
    'XYNProtonsE' + tag    : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 1,0, -50,50,-1,-1, 0, lText, 0.2,0.96, 1e-8,1e-3, ],
    'XYNPiPlusE' + tag     : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, -50,50,-1,-1, 0, lText, 0.2,0.96, 1e-8,5e-4, ],       
    'XYNPiMinusE' + tag    : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 1,0, -50,50,-1,-1, 0, lText, 0.2,0.96, 1e-8,5e-4, ],
    'XYNKaonPlusE' + tag   : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, -50,50,-1,-1, 0, lText, 0.2,0.96, 1e-8,3e-5, ],
    'XYNKaonMinusE' + tag  : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 1,0, -50,50,-1,-1, 0, lText, 0.2,0.96, 1e-8,3e-5, ],
    }
# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'beamgas 3.5 TeV'
tag = tag_BG_3p5TeV
#
lText = 'beamgas 4 TeV'
tag = tag_BG_4TeV
if tag.count('bs'): lText = '4 TeV BG with beamsize'

lText = 'beamgas 6.5 TeV'
tag = tag_BG_6p5TeV
if tag.count('bs'): lText = '6.5 TeV BG with beamsize'

hDict_BG_4TeV = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.65, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-4,10., 0, lText, 0.2,0.9, -1,-1, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9, -1,-1, ],
    'EkinChar' + tag : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinBp' + tag : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-4,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinPiInBp' + tag : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.65, 0.7, 0.98, 0.9, 0,1, 0,600,1e-9,1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadNDistTEST' + tag: [ ['RadNMuons', 'RadNNeutrons'],0.65, 0.7, 0.98, 0.9, 0,1, -1,-1,1e-13,1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100', 'RadNMuonsE500'],0.52, 0.72, 0.95, 0.88, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.956, -1,-1, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnProtons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1190.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.65, 0.65, 0.98, 0.9, 0,1, 0,600,1e-9,2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, 3.14,3.01,3e-3,100, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, 3.14,3.01,-1,-1, 1, lText, 0.2,0.9, -1,-1, ], 

    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.44, 0.68, 0.98, 0.9, 0,1, 3.14,3.01,1e-2,1e4, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR100','PhiEnMuR200','PhiEnMuR500','PhiEnMuR1000'],0.3, 0.73, 0.6, 0.95, 0,1, -3.14,3.,1e-4,5, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuE' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnMuE100'],0.6, 0.78, 0.9,0.92, 0,1, 3.14,3.01,1e-2,1e4, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200','PhiEnMuRlt500','PhiEnMuRlt1000'],0.6, 0.72, 0.9,0.92, 0,1, 3.14,3.01,1e-5,1e2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuRlt200' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200'],0.6, 0.72, 0.9,0.92, 0,1, 3.14,3.01,1e-5,1e2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNMuPM' + tag: [ ['PhiNMuons','PhiNMuPlus','PhiNMuMinus'],0.4, 0.64, 0.7, 0.92, 0,1, -3.14,3.,1e-5,9-1, 1, lText, 0.2,0.955, -1,-1, ],    
    'PhiEnMuPM' + tag : [ ['PhiEnMuons', 'PhiEnMuPlus', 'PhiEnMuMinus'],0.65, 0.7, 0.98, 0.9, 0,1, -3.14,3.,2e-2,5, 0, lText, 0.2,0.955, -1,-1, ],
    
    'XcoorNChar' + tag: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'YcoorNChar' + tag: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'XYNAll' + tag           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNAllZoom' + tag       : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -15,15,-15,15, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuonsE10' + tag      : [ ['XYNMuonsE10'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuonsE500' + tag     : [ ['XYNMuonsE500'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNChar' + tag          : [ ['XYNChar'],0.5, 0.88, 0.7, 1., 1,0, -1,1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNCharZoom' + tag      : [ ['XYNChar'],0.5, 0.83, 0.7, 1., 1,0, -15,15,-15,15, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNProtons' + tag       : [ ['XYNProtons'], 0.5, 0.88, 0.83, 0.92, 1, 0, -30, 30, -30, 30, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNProtonsE10' + tag   : [ ['XYNProtonsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNProtonsE100' + tag   : [ ['XYNProtonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNProtonsE500' + tag   : [ ['XYNProtonsE500'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.75, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsZoom' + tag    : [ ['XYNPhotons'], 0.75, 0.88, 0.83, 0.92, 1,0, -15,15,-15,15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsE10' + tag     : [ ['XYNPhotonsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsE100' + tag    : [ ['XYNPhotonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNNeutrons' + tag       : [ ['XYNNeutrons'], 0.75, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNNeutronsE10' + tag     : [ ['XYNNeutronsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNNeutronsE100' + tag    : [ ['XYNNeutronsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -15, 15, -15, 15, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNNeutronsE' + tag      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNProtonsE' + tag       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNPiPlusE' + tag        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],       
    'XYNPiMinusE' + tag       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNKaonPlusE' + tag      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNKaonMinusE' + tag     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'OrigXYMuons' + tag       : [ ['OrigXYMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigXZMuons' + tag       : [ ['OrigXZMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigYZMuons' + tag       : [ ['OrigYZMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigXYMuonsE100' + tag       : [ ['OrigXYMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigXZMuonsE100' + tag       : [ ['OrigXZMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigYZMuonsE100' + tag       : [ ['OrigYZMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],

    'PhiNAllZ' + tag      : [ ['PhiNAll','PhiNAllZ1', 'PhiNAllZ2', 'PhiNAllZ3', 'PhiNAllZ4'],0.25, 0.7, 0.6, 0.85, 0,1, 3.14,3.01,1e-4,699, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnAllZ' + tag      : [ ['PhiEnAll','PhiEnAllZ1', 'PhiEnAllZ2', 'PhiEnAllZ3', 'PhiEnAllZ4'],0.26, 0.7, 0.6, 0.85, 0,1, 3.14,3.01,1e-1,1e3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNProtonsZ' + tag      : [ ['PhiNProtons','PhiNPrZ1', 'PhiNPrZ2', 'PhiNPrZ3', 'PhiNPrZ4'],0.25, 0.7, 0.6, 0.85, 0,1, 3.14,3.01,1e-4,99, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnProtonsZ' + tag      : [ ['PhiEnProtons','PhiEnPrZ1', 'PhiEnPrZ2', 'PhiEnPrZ3', 'PhiEnPrZ4'],0.26, 0.7, 0.6, 0.85, 0,1, 3.14,3.01,1e-1,1e3, 0, lText, 0.2,0.9, -1,-1, ],

    'PhiNMuonsZR1' + tag      : [ ['PhiNMuonsZ1R1', 'PhiNMuonsZ2R1', 'PhiNMuonsZ3R1', 'PhiNMuonsZ4R1'],0.3, 0.7, 0.95, 0.85, 0,1, 3.14,3.01,3e-7,9e-3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuonsZR1' + tag     : [ ['PhiEnMuonsZ1R1', 'PhiEnMuonsZ2R1', 'PhiEnMuonsZ3R1', 'PhiEnMuonsZ4R1'],0.3, 0.7, 0.95, 0.88, 0,1, 3.14,3.01,1e-5,20, 0, lText, 0.2,0.9, -1,-1, ],

    'PhiNMuonsZR2' + tag      : [ ['PhiNMuonsZ1R2', 'PhiNMuonsZ2R2', 'PhiNMuonsZ3R2', 'PhiNMuonsZ4R2'],0.13, 0.7, 0.95, 0.85, 0,1, 3.14,3.01,3e-7,9e-3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuonsZR2' + tag     : [ ['PhiEnMuonsZ1R2', 'PhiEnMuonsZ2R2', 'PhiEnMuonsZ3R2', 'PhiEnMuonsZ4R2'],0.13, 0.7, 0.95, 0.88, 0,1, 3.14,3.01,1e-5,20, 0, lText, 0.2,0.9, -1,-1, ],

    'PhiNMuonsZR1E100' + tag      : [ ['PhiNMuonsZ1R1E100', 'PhiNMuonsZ2R1E100', 'PhiNMuonsZ3R1E100', 'PhiNMuonsZ4R1E100'],0.3, 0.7, 0.95, 0.85, 0,1, 3.14,3.01,3e-7,9e-3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuonsZR1E100' + tag     : [ ['PhiEnMuonsZ1R1E100', 'PhiEnMuonsZ2R1E100', 'PhiEnMuonsZ3R1E100', 'PhiEnMuonsZ4R1E100'],0.3, 0.7, 0.95, 0.88, 0,1, 3.14,3.01,1e-5,20, 0, lText, 0.2,0.9, -1,-1, ],

    'PhiNMuonsZR2E100' + tag      : [ ['PhiNMuonsZ1R2E100', 'PhiNMuonsZ2R2E100', 'PhiNMuonsZ3R2E100', 'PhiNMuonsZ4R2E100'],0.3, 0.7, 0.95, 0.85, 0,1, 3.14,3.01,3e-7,9e-3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuonsZR2E100' + tag     : [ ['PhiEnMuonsZ1R2E100', 'PhiEnMuonsZ2R2E100', 'PhiEnMuonsZ3R2E100', 'PhiEnMuonsZ4R2E100'],0.3, 0.7, 0.95, 0.88, 0,1, 3.14,3.01,1e-5,20, 0, lText, 0.2,0.9, -1,-1, ],

    'OrigZ' + tag       : [ ['OrigZPhotons', 'OrigZProtons','OrigZMuon'],0.75, 0.88, 0.83, 0.92, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'OrigZE100' + tag       : [ ['OrigZPhotE100', 'OrigZPrE100','OrigZMuE100'],0.75, 0.88, 0.83, 0.92, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],

    }

# --------------------------------------------------------------------------------------------------------------------------------------------------------
tag = tag_BH_3p5TeV
Beam, beam, beamn = getBeam(tag)
lText = Beam + ' beamhalo 3.5 TeV'
hDict_BH_3p5TeV = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, -1,-1, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9, -1,-1, ],
    'EkinChar' + tag : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinBp' + tag : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'EkinPiInBp' + tag : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,600,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE500'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.9, -1,-1, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0, 200,1e-5,1, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-5,1e1, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-3,1e2, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,1e-5,1, 1, lText, 0.2,0.9, -1,-1, ], 
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.6, 0.6, 0.9,0.9, 0,1, -1,-1,1e-5,1e3, 0, lText, 0.2,0.9, -1,-1, ],
    'PhiEnMuE' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnMuE100'],0.6, 0.72, 0.9,0.92, 0,1, -1,-1,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200','PhiEnMuRlt500','PhiEnMuRlt1000'],0.6, 0.72, 0.9,0.92, 0,1, -1,-1,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt200' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200'],0.6, 0.72, 0.9,0.92, 0,1, -1,-1,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,1e-3,1e2, 0, lText, 0.2,0.9, -1,-1, ],

    'XcoorNChar' + tag: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, -1,-1, ],
    'YcoorNChar' + tag: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, -1,-1, ],

    'XYNAll' + tag           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 1,0, -30,30,-30,30, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuonsE10' + tag      : [ ['XYNMuonsE10'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuonsE100' + tag     : [ ['XYNMuonsE100'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNChar' + tag          : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, -30,30,-30,30, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNCharZoom' + tag      : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, -6.,6.,6.,6., 0, lText, 0.2,0.9, -1,-1, ],
    'XYNProtons' + tag         : [ ['XYNProtons'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNProtonsE10' + tag      : [ ['XYNProtonsE10'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNProtonsE100' + tag     : [ ['XYNProtonsE100'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],


    'XYNNeutronsE' + tag      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNProtonsE' + tag       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNPiPlusE' + tag        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],       
    'XYNPiMinusE' + tag       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-4,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNKaonPlusE' + tag      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNKaonMinusE' + tag     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],

    'OrigXYMuons' + tag       : [ ['OrigXYMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigXZMuons' + tag       : [ ['OrigXZMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigYZMuons' + tag       : [ ['OrigYZMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigXYMuonsE100' + tag       : [ ['OrigXYMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigXZMuonsE100' + tag       : [ ['OrigXZMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigYZMuonsE100' + tag       : [ ['OrigYZMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],

    }


# --------------------------------------------------------------------------------------------------------------------------------------------------------

def generateHybridDicts(tag,ccf,lText):

    hDict_hybrid = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx (label) #14 ly (label) #15 ZurMin #16 ZurMax
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.65, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-5,1*ccf, 0, lText, 0.16,0.96, -1,-1, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.65, 0.7, 0.98, 0.9, 0,1, 0,600,-1,-1, 0, lText, 0.2,0.955, -1,-1, ],
    'RadNChar' + tag: [ ['RadNPhotons','RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.955, -1,-1, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE500'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.955, -1,-1, ],
    'RadEnChar' + tag: [ ['RadEnPhotons','RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons'],0.6, 0.7, 0.9, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.955, -1,-1, ],
    'RadEnCharZoom' + tag: [ ['RadEnPhotons','RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons'],0.6, 0.7, 0.9, 0.9, 0,1, 0.,15.,1e-7,1.*ccf, 0, lText, 0.2,0.955, -1,-1, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.65, 0.65, 0.98, 0.9, 0,1, 0,600,1e-9,1*ccf, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.65, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-5*ccf,1*ccf, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-3*ccf,1e2*ccf, 0, lText, 0.2,0.955, -1,-1, ],
    'RadEnDistZoom' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.65, 0.65, 0.98, 0.9, 0,1, 0,15,1e-5,1*ccf, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,1e-5,1, 1, lText, 0.2,0.955, -1,-1, ], 
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.6, 0.6, 0.9,0.9, 0,1, -1,-1,1e-5,1e3, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.65, 0.7, 0.98, 0.9, 0,1, -1,-1,1e-3*ccf,1e2*ccf*ccf, 0, lText, 0.2,0.955, -1,-1, ],

    'ZcoorOrigMu' + tag: [ ['ZcoorOrigMu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e-2, 0, lText, 0.2,0.95, -1,-1, ],
    'XYEnMuons' + tag : [['XYEnMuons'],0.5, 0.8, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNAll' + tag           : [ ['XYNAll'],0.75, 0.88, 0.83, 0.92, 1,0, -30,30,-30,30, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.75, 0.88, 0.83, 0.92, 1, 0, -1, -1, -1, -1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNMuonsE100' + tag     : [ ['XYNMuonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -1, -1, -1, -1, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNProtons' + tag       : [ ['XYNProtons'], 0.5, 0.88, 0.83, 0.92, 1, 0, -30, 30, -30, 30, 0, lText, 0.2,0.96, 6e-7,1e-4, ],
    'XYNProtonsE10' + tag   : [ ['XYNProtonsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 1e-7,1e-5, ],
    'XYNProtonsE100' + tag   : [ ['XYNProtonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 1e-7,1e-5, ],
    'XYNProtonsE500' + tag   : [ ['XYNProtonsE500'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 1e-7,1e-4, ],

    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.75, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNPhotonsE10' + tag     : [ ['XYNPhotonsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 6e-7,1e-4, ],
    'XYNPhotonsE100' + tag    : [ ['XYNPhotonsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 6e-7,1e-4, ],

    'XYNNeutrons' + tag       : [ ['XYNNeutrons'], 0.75, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNNeutronsE10' + tag     : [ ['XYNNeutronsE10'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 6e-7,1e-4, ],
    'XYNNeutronsE100' + tag    : [ ['XYNNeutronsE100'], 0.5, 0.88, 0.83, 0.92, 1, 0, -10, 10, -10, 10, 0, lText, 0.2,0.96, 6e-7,1e-4, ],

    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.88, 0.83, 0.92, 1,0, -10, 10, -10, 10, 0, lText, 0.2,0.96, -1,-1, ],

    'XYNChar' + tag          : [ ['XYNChar'],0.5, 0.88, 0.83, 0.92, 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, -1,-1, ],
    'XYNCharZoom2' + tag     : [ ['XYNChar'],0.5, 0.88, 0.83, 0.92, 1,0, -5,5,-5.,5., 0, lText, 0.2,0.96, 2e-5, 1e-2, ],
    'XYNCharZoom' + tag      : [ ['XYNChar'],0.5, 0.88, 0.83, 0.92, 1,0, -15,15,-15.,15., 0, lText, 0.2,0.96, 1e-7,1e-4, ],

    'OrigXYMuons' + tag       : [ ['OrigXYMuon'],0.75, 0.88, 0.83, 0.92, 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigXZMuons' + tag       : [ ['OrigXZMuon'],0.75, 0.88, 0.83, 0.92, 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigYZMuons' + tag       : [ ['OrigYZMuon'],0.75, 0.88, 0.83, 0.92, 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigXYMuonsE100' + tag       : [ ['OrigXYMuonsE100'],0.5, 0.88, 0.83, 0.92, 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigXZMuonsE100' + tag       : [ ['OrigXZMuonsE100'],0.5, 0.88, 0.83, 0.92, 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigYZMuonsE100' + tag       : [ ['OrigYZMuonsE100'],0.5, 0.88, 0.83, 0.92, 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.96, 8e-7,8e-3, ],

    'OrigZ' + tag       : [ ['OrigZPhotons', 'OrigZProtons','OrigZMuons'],0.75, 0.88, 0.83, 0.92, 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    'OrigZE100' + tag       : [ ['OrigZPhotE100', 'OrigZPrE100','OrigZMuE100'],0.75, 0.88, 0.83, 0.92, 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.96, 8e-7,8e-3, ],
    }

    return hDict_hybrid
# .................................................................................

tag = tag_BH_7TeV

collsett = 'retracted sett,'

Beam, beam, beamn = getBeam(tag)
if tag.count("nom"): collsett = 'nom sett,'
if tag.count('tct5ot'): lText = 'HL TCT5 out, TCT4 in, round B' + beamn
else: #lText = 'HL Halo TCT4+5 in,'+collsett+' rd B'+beamn
    lText = 'HL Halo TCT5s in,'+collsett+' rd B'+beamn
ccf = 1.
hDict_HL_BH_hybrid = generateHybridDicts(tag,ccf,lText)

tag = tag_crab_HL
#lText = 'crabs phase flip mod TAXN'
if tag.count("crab"): 
    ccf = 20
    lText = 'HL crabs phase flip, nom sett, B1'

hDict_HL_crabs_hybrid =  generateHybridDicts(tag,ccf,lText)

# --------------------------------------------------------------------------------------------------------------------------------------------------------
hDict_HLhybrid_comp = {

    # ---------------------------------------------------------------------------------
    # comp plots
    # ---------------------------------------------------------------------------------
    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly #15 ZurMin #16 ZurMax

    'EkinAllComp' : [['EkinAllIN', 'EkinAllOUT' ],0.55,0.77,0.95,0.9, 1,1, 2e-2,9e3,1,1.e10, 0, '', 0.45,0.85, -1,-1, ],
    'EkinNeComp' : [['EkinNeIN', 'EkinNeOUT' ],0.55,0.77,0.95,0.9, 1,1, 2e-2,9e3,1,1.e10, 0, 'n', 0.45,0.85, -1,-1, ],
    'EkinPrComp' : [['EkinPrIN', 'EkinPrOUT' ],0.55,0.77,0.95,0.9, 1,1, 2e-2,9e3,1,1.e10, 0, 'p', 0.45,0.85, -1,-1, ],
    'EkinMuComp' : [['EkinMuIN', 'EkinMuOUT' ],0.55,0.77,0.95,0.9, 1,1, 2e-2,9e3,1,1.e10, 0, '#mu^{#pm}', 0.45,0.85, -1,-1, ],
    'RadEnAllComp' : [['RadEnAllIN','RadEnAllOUT'], 0.55,0.77,0.95,0.9, 0,1, 0.,600.,1,8e8, 0, 'all', 0.45,0.85, -1,-1, ],
    'RadEnChComp' :  [['RadEnChIN','RadEnChOUT'], 0.55,0.77,0.95,0.9, 0,1, 0.,600.,1,8e8, 0, '#pi^{#pm}, K^{#pm}', 0.45,0.85, -1,-1, ],
    'RadEnMuComp' :  [['RadEnMuIN','RadEnMuOUT'], 0.55,0.77,0.95,0.9, 0,1, 0.,600.,1,8e8, 0, '#mu^{#pm}', 0.45,0.85, -1,-1, ],
    'RadNMuComp' :  [['RadNMuIN','RadNMuOUT'], 0.55,0.77,0.95,0.9, 0,1, 0.,600.,1e-2,8e2, 0, '#mu^{#pm}', 0.45,0.85, -1,-1, ],
    'PhiNAllComp' :  [['PhiNAllIN','PhiNAllOUT'], 0.55,0.77,0.95,0.9, 0,1, -math.pi, math.pi-0.5*math.pi,3e6,1.e8, 0, 'all', 0.45,0.85, -1,-1, ],
    }

# --------------------------------------------------------------------------------------------------------------------------------------------------------
tag = tag_BH_6p5TeV
Beam, beam, beamn = getBeam(tag)
lText = "BH 6.5 TeV B"+beamn
hDict_BH_6p5TeV = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx (label) #14 ly (label) #15 ZurMin #16 ZurMax
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.65, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-5,1, 0, lText, 0.16,0.96, -1,-1, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.65, 0.7, 0.98, 0.9, 0,1, 0,600,-1,-1, 0, lText, 0.2,0.955, -1,-1, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.955, -1,-1, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE500'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.955, -1,-1, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.6, 0.7, 0.9, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.955, -1,-1, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.65, 0.65, 0.98, 0.9, 0,1, 0,600,1e-9,1, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.65, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-5,1e1, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons', 'PhiEnProtons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-3,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,1e-5,1, 1, lText, 0.2,0.955, -1,-1, ],

    'PhiNMuE' + tag: [ ['PhiNProtons','PhiNMuons','PhiNMuE100'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,1e-5,1, 1, lText, 0.2,0.955, -1,-1, ], 
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR100','PhiEnMuR200','PhiEnMuR500','PhiEnMuR1000'],0.3, 0.73, 0.6, 0.95, 0,1, -3.14,3.,1e-4,15, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuE' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnMuE100'],0.6, 0.78, 0.9,0.92, 0,1, -1,-1,1e-2,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200','PhiEnMuRlt500','PhiEnMuRlt1000'],0.6, 0.72, 0.9,0.92, 0,1, -1,-1,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnMuRlt200' + tag: [ ['PhiEnMuons','PhiEnMuRlt10','PhiEnMuRlt50','PhiEnMuRlt100','PhiEnMuRlt200'],0.6, 0.72, 0.9,0.92, 0,1, -1,-1,1e-5,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    'PhiEnDist' + tag:[[ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.65, 0.7, 0.98, 0.9, 0,1, -1,-1,1e-3,1e2, 0, lText, 0.2,0.955, -1,-1, ],
    
    'PhiNMuPM' + tag: [ ['PhiNMuons','PhiNMuPlus','PhiNMuMinus'],0.4, 0.64, 0.7, 0.92, 0,1, -3.14,3.,1e-5,9-1, 1, lText, 0.2,0.955, -1,-1, ],    
    'PhiEnMuPM' + tag : [ ['PhiEnMuons', 'PhiEnMuPlus', 'PhiEnMuMinus'],0.65, 0.7, 0.98, 0.9, 0,1, -3.14,3.,2e-2,5, 0, lText, 0.2,0.955, -1,-1, ], 

    'ZcoorOrigMu' + tag: [ ['ZcoorOrigMu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e-2, 0, lText, 0.2,0.9, -1,-1, ],

    'XYEnMuons' + tag: [['XYEnMuons'],0.5, 0.92, 0.7, 1., 1,0, -30,30,-30,30, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNAll' + tag           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 1,0, -30,30,-30,30, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 1, 0, -1, -1, -1, -1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuonsE10' + tag      : [ ['XYNMuonsE10'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNMuonsE500' + tag     : [ ['XYNMuonsE500'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNChar' + tag          : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, -1,-1, ],
    'XYNCharZoom' + tag      : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, -5,5,-5.,5., 0, lText, 0.2,0.9, -1,-1, ],

    'OrigXYMuons' + tag       : [ ['OrigXYMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigXZMuons' + tag       : [ ['OrigXZMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigYZMuons' + tag       : [ ['OrigYZMuon'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigXYMuonsE100' + tag       : [ ['OrigXYMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigXZMuonsE100' + tag       : [ ['OrigXZMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'OrigYZMuonsE100' + tag       : [ ['OrigYZMuonsE100'],0.5, 0.92, 0.7, 1., 1,0, -1,-1, -80, 80, 0, lText, 0.2,0.9, 8e-7,8e-3, ],

    'ProfOrigXZMuons' + tag       : [ ['ProfOrigXZMuon'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    'ProfOrigYZMuons' + tag       : [ ['ProfOrigYZMuon'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, 8e-7,8e-3, ],
    }
