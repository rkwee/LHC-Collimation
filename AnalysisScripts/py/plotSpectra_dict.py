Beam = 'B1'
tag_HL   = 'HL_BH'
# ---------------------------------------------------------------------------------
# dict for histograms, ALL hDicts must have the same structure!!
# ---------------------------------------------------------------------------------
hDict_HL_comp = {

    # ---------------------------------------------------------------------------------
    # comp plots
    # ---------------------------------------------------------------------------------
    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly

    'EkinMuComp' : [['EkinMuBGst', 'EkinMuBGac', 'EkinMuBHds', 'EkinMuBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, '#mu^{#pm}', 0.55,0.85],
    'EkinPrComp' : [['EkinPrBGst', 'EkinPrBGac', 'EkinPrBHds', 'EkinPrBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, 'p', 0.55,0.85],
    'EkinPhComp' : [['EkinPhBGst', 'EkinPhBGac', 'EkinPhBHds', 'EkinPhBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, '#gamma', 0.55,0.85],
    'EkinEpComp' : [['EkinEpBGst', 'EkinEpBGac', 'EkinEpBHds', 'EkinEpBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, 'e^{#pm}', 0.55,0.85],
    'EkinNeComp' : [['EkinNeBGst', 'EkinNeBGac', 'EkinNeBHds', 'EkinNeBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, 'n', 0.55,0.85],
    'EkinChComp' : [['EkinChBGst', 'EkinChBGac', 'EkinChBHds', 'EkinChBHop' ],0.63,0.73,0.95,0.9, 1,1, 2e-2,9e3,1e-1,8e9, 0, '#pi^{#pm}, K^{#pm}', 0.55,0.85],

    'RadNMuComp' : [['RadNMuBGst', 'RadNMuBGac', 'RadNMuBHds', 'RadNMuBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, '#mu^{#pm}', 0.55,0.85],
    'RadNPrComp' : [['RadNPrBGst', 'RadNPrBGac', 'RadNPrBHds', 'RadNPrBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, 'p', 0.55,0.85],
    'RadNPhComp' : [['RadNPhBGst', 'RadNPhBGac', 'RadNPhBHds', 'RadNPhBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, '#gamma', 0.55,0.85],
    'RadNEpComp' : [['RadNEpBGst', 'RadNEpBGac', 'RadNEpBHds', 'RadNEpBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, 'e^{#pm}', 0.55,0.85],
    'RadNNeComp' : [['RadNNeBGst', 'RadNNeBGac', 'RadNNeBHds', 'RadNNeBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, 'n', 0.55,0.85],
    'RadNChComp' : [['RadNChBGst', 'RadNChBGac', 'RadNChBHds', 'RadNChBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-5,9e7, 0, '#pi^{#pm}, K^{#pm}', 0.55,0.85],

    'RadEnMuComp' : [['RadEnMuBGst', 'RadEnMuBGac', 'RadEnMuBHds', 'RadEnMuBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, '#mu^{#pm}', 0.55,0.85],
    'RadEnPrComp' : [['RadEnPrBGst', 'RadEnPrBGac', 'RadEnPrBHds', 'RadEnPrBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, 'p', 0.55,0.85],
    'RadEnPhComp' : [['RadEnPhBGst', 'RadEnPhBGac', 'RadEnPhBHds', 'RadEnPhBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, '#gamma', 0.55,0.85],
    'RadEnEpComp' : [['RadEnEpBGst', 'RadEnEpBGac', 'RadEnEpBHds', 'RadEnEpBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, 'e^{#pm}', 0.55,0.85],
    'RadEnNeComp' : [['RadEnNeBGst', 'RadEnNeBGac', 'RadEnNeBHds', 'RadEnNeBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, 'n', 0.55,0.85],
    'RadEnChComp' : [['RadEnChBGst', 'RadEnChBGac', 'RadEnChBHds', 'RadEnChBHop' ],0.63,0.73,0.95,0.9, 0,1, 0,600.,2e-8,9e8, 0, '#pi^{#pm}, K^{#pm}', 0.55,0.85],

}

# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'beamhalo'
tag_HL= '_BH'
hDict_HL_BH = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    # 'Ekin_debug_TCT' : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'], 0.72,0.7,0.98,0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.7, ],
    # 'RadNChar_debug_TCT': [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-6,1, 0, lText, 0.2,0.7, ],

    'Ekin' + tag_HL : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9],
    'EkinChar' + tag_HL : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, ],
    'EkinBp' + tag_HL : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, ],
    'EkinPiInBp' + tag_HL : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 0, lText, 0.2,0.9, ],

    'RadNDist' + tag_HL: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,1200,-1,-1, 0, lText, 0.2,0.9, ],
    'RadNChar' + tag_HL: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-5,2, 0, lText, 0.2,0.9, ],

    'RadNMuons' + tag_HL: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE1000'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-8,1e-4, 1, lText, 0.2,0.9, ],
    'RadEnChar' + tag_HL: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,1e-10,1, 0, lText, 0.2,0.9, ],
    'RadEnDist' + tag_HL:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0,1200,1e-10,1, 0, lText, 0.2,0.9, ],
    'PhiNDist' + tag_HL: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-3,9, 0, lText, 0.2,0.9, ],
    'PhiEnChar' + tag_HL: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-2,1e2, 0, lText, 0.2,0.9, ],
    'PhiNMu' + tag_HL: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -3.14,3.,1e-5,9-1, 1, lText, 0.2,0.9, ], 
    'PhiEnMu' + tag_HL: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.2, 0.8, 0.5, 1.0, 0,1, -3.14,3.,1e-5,9-1, 0, lText, 0.2,0.9, ],
    'PhiEnDist' + tag_HL:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,5e-3,5e2, 0, lText, 0.2,0.9, ],

    'XcoorNChar' + tag_HL: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e1, 0, lText, 0.2,0.9, ],
    'YcoorNChar' + tag_HL: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1e1, 0, lText, 0.2,0.9, ],

    'XYNAll' + tag_HL           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNMuons' + tag_HL         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPhotons' + tag_HL       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNElecPosi' + tag_HL      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],

    'XYNNeutronsE' + tag_HL      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNProtonsE' + tag_HL       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPiPlusE' + tag_HL        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],       
    'XYNPiMinusE' + tag_HL       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonPlusE' + tag_HL      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonMinusE' + tag_HL     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],

    }
lText = 'BG a.c.'
tag_HL = '_BGac'
hDict_HL_BGac = { # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly

    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag_HL : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72,0.7,0.98,0.9, 1,1, 2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1,  2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, ],
    'EkinChar' + tag_HL : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.6,0.7,0.98,0.9, 1,1, 2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9, ],
    'EkinBp' + tag_HL : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6,0.98,0.9, 1,1, 2e-2,1e4,2e2,1e8, 0, lText, 0.7,0.9],
    'EkinPiInBp' + tag_HL : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6,0.98,0.9, 1,1, 2e-2,1e4, 2e2,1e8, 0, lText, 0.7,0.9, ],

    'RadNDist' + tag_HL: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,600,1e-5,1e5, 0, lText, 0.7,0.9, ],
    'RadNChar' + tag_HL: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,1e-5,1e5, 0, lText, 0.7,0.9, ],

    'RadNMuons' + tag_HL: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE1000'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.7,0.9, ],
    'RadEnChar' + tag_HL: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,1e-5,1e9, 0, lText, 0.7,0.9, ],
    'RadEnDist' + tag_HL:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0.,600,1e-5,1e9, 0, lText, 0.7,0.9, ],
    'PhiNDist' + tag_HL: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,1e3,1e8, 0, lText, 0.3,0.9, ],
    'PhiEnChar' + tag_HL: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52,0.75,0.98,0.9, 0,1, -1,-1,1e5,2e10, 0, lText, 0.5,0.9, ],
    'PhiNMu' + tag_HL: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4,0.64,0.7,0.92, 0,1, -1,-1,1e2,1e5, 0, lText, 0.7,0.9, ], 
    'PhiEnMu' + tag_HL: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.2, 0.7, 0.5, 1.0, 0,1, -1,-1,1e1,1e8, 1, lText, 0.7,0.9, ],
    'PhiEnDist' + tag_HL:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,1e3,2e10, 0, lText, 0.3,0.9, ],

    'XcoorNChar' + tag_HL: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-2,1e7, 0, lText, 0.7,0.9, ],
    'YcoorNChar' + tag_HL: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-2,1e7, 0, lText, 0.7,0.9, ],

    'XYNAll' + tag_HL           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNMuons' + tag_HL         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNPhotons' + tag_HL       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNElecPosi' + tag_HL      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],

    'XYNNeutronsE' + tag_HL      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNProtonsE' + tag_HL       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNPiPlusE' + tag_HL        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],       
    'XYNPiMinusE' + tag_HL       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNKaonPlusE' + tag_HL      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],
    'XYNKaonMinusE' + tag_HL     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.7,0.9, ],

    }

# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'beamhalo 4 TeV' 
tag = '_BH_4TeV_' + Beam
hDict_BH_4TeV = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9],
    'EkinChar' + tag : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, ],
    'EkinBp' + tag : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],
    'EkinPiInBp' + tag : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,600,-1,-1, 0, lText, 0.2,0.9, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE1000'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.9, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0,200,1e-5,1, 0, lText, 0.2,0.9, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-5,1e1, 0, lText, 0.2,0.9, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-3,1e2, 0, lText, 0.2,0.9, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,1e-5,1, 1, lText, 0.2,0.9, ], 
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.6, 0.6, 0.9,0.9, 0,1, -1,-1,1e-5,1e3, 0, lText, 0.2,0.9, ],
    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,1e-3,1e2, 0, lText, 0.2,0.9, ],

    'XcoorNChar' + tag: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, ],
    'YcoorNChar' + tag: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, ],

    'XYNAll' + tag           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNChar' + tag          : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-3,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNCharZoom' + tag      : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,8e-4,6.,6., 0, lText, 0.2,0.9, ],

    'XYNNeutronsE' + tag      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNProtonsE' + tag       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPiPlusE' + tag        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-4,-1,-1, 0, lText, 0.2,0.9, ],       
    'XYNPiMinusE' + tag       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-4,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonPlusE' + tag      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonMinusE' + tag     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],

    'XYNMuonsE10' + tag         : [ ['XYNMuonsE10'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    }
# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'beamgas 4 TeV'
tag = '_BG_4TeV'
hDict_BG_4TeV = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9],
    'EkinChar' + tag : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],
    'EkinBp' + tag : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],
    'EkinPiInBp' + tag : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,1200,-1,-1, 0, lText, 0.2,0.9, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 0, lText, 0.2,0.9, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE1000'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 1, lText, 0.2,0.9, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,1200.,-1,-1, 0, lText, 0.2,0.9, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0,1200,-1,-1, 0, lText, 0.2,0.9, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,-1,-1, 0, lText, 0.2,0.9, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,-1,-1, 1, lText, 0.2,0.9, ], 
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.2, 0.8, 0.5, 1.0, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],

    'XcoorNChar' + tag: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'YcoorNChar' + tag: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],

    'XYNAll' + tag           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],

    'XYNNeutronsE' + tag      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNProtonsE' + tag       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPiPlusE' + tag        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],       
    'XYNPiMinusE' + tag       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonPlusE' + tag      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonMinusE' + tag     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 0,0, -1,-1,-1,-1, 0, lText, 0.2,0.9, ],

    }

# --------------------------------------------------------------------------------------------------------------------------------------------------------
lText = 'beamhalo 3.5 TeV'
tag = '_BH_3p5TeV'
hDict_BH_3p5TeV = { 

    # hkey = pname; #0 list of hists #1 legend x1 #2 y1 #3 x2 #4 y2 #5 doLogx #6 doLogy #7 XurMin #8 XurMax #9 YurMin #10 YurMax #11 doFill #12 lText #13 lx #14 ly
    # ---------------------------------------------------------------------------------
    # single file plots
    # ---------------------------------------------------------------------------------

    'Ekin' + tag : [['EkinAll', 'EkinMuons', 'EkinPhotons', 'EkinElecPosi','EkinNeutrons', 'EkinProtons','EkinPions', 'EkinKaons'],0.72, 0.7, 0.98, 0.9, 1,1,2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, ],
    'Ekin_TCT_more' : [[ 'EkinAll','EkinSel3','EkinSel2','EkinSel1','EkinPions', 'EkinKaons'],0.52, 0.75, 0.98, 0.9, 1,1, 2e-2,1e4,1e-6,9, 1, lText, 0.2,0.9],
    'EkinChar' + tag : [[ 'EkinPos','EkinNeg','EkinNeu', 'EkinPiPlus','EkinPiMinus','EkinPhotons'],0.52, 0.7, 0.98, 0.9, 1,1, 2e-2,1e4,1e-5,1, 0, lText, 0.2,0.9, ],
    'EkinBp' + tag : [['EkinAll', 'EkinAllRInBP','EkinPiPlusRInBP','EkinPiMinusRInBP','EkinNeutronsRInBP','EkinAllROutBP','EkinPiPlusROutBP','EkinPiMinusROutBP','EkinNeutronsROutBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],
    'EkinPiInBp' + tag : [['EkinPiPlusRInBP','EkinPiMinusRInBP'],0.7, 0.6, 0.98, 0.9, 1,1, 2e-2,1e4,-1,-1, 0, lText, 0.2,0.9, ],

    'RadNDist' + tag: [ ['RadNAll', 'RadNMuons', 'RadNNeutrons', 'RadNProtons', 'RadNPhotons', 'RadNElecPosi', 'RadNPions', 'RadNKaons'],0.72, 0.7, 0.98, 0.9, 0,1, 0,600,-1,-1, 0, lText, 0.2,0.9, ],
    'RadNChar' + tag: [ ['RadNNeg', 'RadNPos', 'RadNNeu','RadNNeutrons','RadNPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, ],

    'RadNMuons' + tag: [ ['RadNMuonsEAll', 'RadNMuonsE20', 'RadNMuonsE100','RadNMuonsE1000'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 1, lText, 0.2,0.9, ],
    'RadEnChar' + tag: [ ['RadEnNeg', 'RadEnPos', 'RadEnNeu','RadEnNeutrons','RadEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, 0.,600.,-1,-1, 0, lText, 0.2,0.9, ],
    'RadEnDist' + tag:[ ['RadEnAll', 'RadEnMuons', 'RadEnNeutrons', 'RadEnProtons', 'RadEnPhotons', 'RadEnElecPosi', 'RadEnPions','RadEnKaons'],0.72, 0.65, 0.98, 0.9, 0,1, 0,200,1e-5,1, 0, lText, 0.2,0.9, ],
    'PhiNDist' + tag: [ ['PhiNAll', 'PhiNMuons','PhiNNeutrons','PhiNProtons','PhiNPhotons', 'PhiNElecPosi', 'PhiNPionsChar', 'PhiNKaonsChar'],0.72, 0.74, 0.98, 0.92, 0,1, -1,-1,1e-5,1e1, 0, lText, 0.2,0.9, ],
    'PhiEnChar' + tag: [ ['PhiEnNeg', 'PhiEnPos', 'PhiEnNeu','PhiEnNeutrons','PhiEnPhotons'],0.52, 0.75, 0.98, 0.9, 0,1, -1,-1.,1e-3,1e2, 0, lText, 0.2,0.9, ],
    'PhiNMu' + tag: [ ['PhiNMuons','PhiNMuR10','PhiNMuR50','PhiNMuR100','PhiNMuR200','PhiNMuR300','PhiNMuR400','PhiNMuR500','PhiNMuR1000'],0.4, 0.64, 0.7, 0.92, 0,1, -1,-1,1e-5,1, 1, lText, 0.2,0.9, ], 
    'PhiEnMu' + tag: [ ['PhiEnMuons','PhiEnMuR10','PhiEnMuR50','PhiEnMuR100','PhiEnMuR200','PhiEnMuR300','PhiEnMuR400','PhiEnMuR500','PhiEnMuR1000'],0.6, 0.6, 0.9,0.9, 0,1, -1,-1,1e-5,1e3, 0, lText, 0.2,0.9, ],
    'PhiEnDist' + tag:[ [ 'PhiEnAll', 'PhiEnMuons', 'PhiEnNeutrons', 'PhiEnProtons', 'PhiEnPhotons', 'PhiEnElecPosi', 'PhiEnPions','PhiEnKaons'],0.72, 0.7, 0.98, 0.9, 0,1, -1,-1,1e-3,1e2, 0, lText, 0.2,0.9, ],


    'XcoorNChar' + tag: [ ['XcoorNNeg', 'XcoorNPos', 'XcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, ],
    'YcoorNChar' + tag: [ ['YcoorNNeg', 'YcoorNPos', 'YcoorNNeu'],0.7, 0.75, 0.98, 0.9, 0,1, -1,-1,1e-6,1, 0, lText, 0.2,0.9, ],

    'XYNAll' + tag           : [ ['XYNAll'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNMuons' + tag         : [ ['XYNMuons'], 0.5, 0.92, 0.7, 1., 1,0, 5e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPhotons' + tag       : [ ['XYNPhotons'], 0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNElecPosi' + tag      : [ ['XYNElecPosi'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,2e-1,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNChar' + tag          : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-3,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNCharZoom' + tag      : [ ['XYNChar'],0.5, 0.92, 0.7, 1., 1,0, 1e-5,8e-4,6.,6., 0, lText, 0.2,0.9, ],

    'XYNNeutronsE' + tag      : [ ['XYNNeutronsE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNProtonsE' + tag       : [ ['XYNProtonsE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNPiPlusE' + tag        : [ ['XYNPiPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-4,-1,-1, 0, lText, 0.2,0.9, ],       
    'XYNPiMinusE' + tag       : [ ['XYNPiMinusE']  ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,2e-4,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonPlusE' + tag      : [ ['XYNKaonPlusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],
    'XYNKaonMinusE' + tag     : [ ['XYNKaonMinusE'] ,0.5, 0.92, 0.7, 1., 1,0, 1e-7,5e-6,-1,-1, 0, lText, 0.2,0.9, ],

    }
