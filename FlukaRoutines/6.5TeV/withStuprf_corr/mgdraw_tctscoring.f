*$ CREATE MGDRAW.FOR
*COPY MGDRAW
*                                                                      *
*=== mgdraw ===========================================================*
*                                                                      *
      SUBROUTINE MGDRAW ( ICODE, MREG )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1990-2006      by        Alfredo Ferrari           *
*     All Rights Reserved.                                             *
*                                                                      *
*                                                                      *
*     MaGnetic field trajectory DRAWing: actually this entry manages   *
*                                        all trajectory dumping for    *
*                                        drawing                       *
*                                                                      *
*     Created on   01 march 1990   by        Alfredo Ferrari           *
*                                              INFN - Milan            *
*     Last change  05-may-06       by        Alfredo Ferrari           *
*                                              INFN - Milan            *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE '(CASLIM)'
      INCLUDE '(COMPUT)'
      INCLUDE '(SOURCM)'
      INCLUDE '(FHEAVY)'
* Start_Devel_seq
      INCLUDE '(FLKMAT)'
* End_Devel_seq
      INCLUDE '(FLKSTK)'
      INCLUDE '(GENSTK)'
      INCLUDE '(MGDDCM)'
      INCLUDE '(PAPROP)'
      INCLUDE '(QUEMGD)'
      INCLUDE '(SUMCOU)'
      INCLUDE '(TRACKR)'
*
*     DIMENSION DTQUEN ( MXTRCK, MAXQMG )
*
      INTEGER NBGEVT
      SAVE NBGEVT
*     CHARACTER*20 FILNAM
      CHARACTER*8 REGNAM
      LOGICAL LFCOPE, LFIRST
      SAVE LFCOPE, LFIRST
      DATA LFCOPE / .TRUE. /, LFIRST / .TRUE. /
*
*----------------------------------------------------------------------*
*                                                                      *
*     Icode = 1: call from Kaskad                                      *
*     Icode = 2: call from Emfsco                                      *
*     Icode = 3: call from Kasneu                                      *
*     Icode = 4: call from Kashea                                      *
*     Icode = 5: call from Kasoph                                      *
*                                                                      *
*----------------------------------------------------------------------*
*                                                                      *
      RETURN
*
*======================================================================*
*                                                                      *
*     Boundary-(X)crossing DRAWing:                                    *
*                                                                      *
*     Icode = 1x: call from Kaskad                                     *
*             19: boundary crossing                                    *
*     Icode = 2x: call from Emfsco                                     *
*             29: boundary crossing                                    *
*     Icode = 3x: call from Kasneu                                     *
*             39: boundary crossing                                    *
*     Icode = 4x: call from Kashea                                     *
*             49: boundary crossing                                    *
*     Icode = 5x: call from Kasoph                                     *
*             59: boundary crossing                                    *
*                                                                      *
*======================================================================*
*                                                                      *
      ENTRY BXDRAW ( ICODE, MREG, NEWREG, XSCO, YSCO, ZSCO )
*
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@                                                            @@@
      IF( LFCOPE ) THEN
*     @@@                                                            @@@
         REGNAM='SCOreg1'
         CALL GEON2R ( REGNAM, MSCOREGS, IERR )
         REGNAM='SCOreg2'
         CALL GEON2R ( REGNAM, MSCOREGE, IERR )
*     @@@                                                            @@@
         WRITE(30, *) "# Scoring from Region No ",MSCOREGS , 
     &                " to ",MSCOREGE
         WRITE(30, *) "# Col  1: primary event number"
         WRITE(30, *) "# -- Particle information --"
         WRITE(30, *) "# Col  2: FLUKA particle type ID"
         WRITE(30, *) "# Col  3: generation number"
         WRITE(30, *) "# Col  4: statistical weight"
         WRITE(30, *) "# -- Crossing at scoring plane --"
         WRITE(30, *) "# Col  5: x coord (cm)"
         WRITE(30, *) "# Col  6: y coord (cm)"
         WRITE(30, *) "# Col  7: x dir cosine"
         WRITE(30, *) "# Col  8: y dir cosine"
         WRITE(30, *) "# Col  9: total energy (GeV)"
         WRITE(30, *) "# Col 10: kinetic energy (GeV)"
         WRITE(30, *) "# Col 11: particle age since primary event (sec)"
         WRITE(30, *) "# -- Primary event --"
         WRITE(30, *) "# Col 12: x coord TCT impact (cm)"
         WRITE(30, *) "# Col 13: y coord TCT impact (cm)"
         WRITE(30, *) "# Col 14: z coord TCT impact (cm)"
         WRITE(30, *) "# Col 15: x coord muon origin (cm)"
         WRITE(30, *) "# Col 16: y coord muon origin (cm)"
         WRITE(30, *) "# Col 17: z coord muon origin (cm)"
*     @@@                                                            @@@
         LFCOPE=.FALSE.
*     @@@                                                            @@@
      END IF
*     @@@                                                            @@@
*     @@@                                                            @@@
      IF ( MREG.EQ.MSCOREGS .AND. NEWREG.EQ.MSCOREGE ) THEN
*     @@@                                                            @@@
         WRITE(30,'(3(I5),14(1PE24.16))') 
     &              ISPUSR(1), JTRACK, LTRACK, WTRACK, 
     &              XSCO, YSCO, CXTRCK, CYTRCK, 
     &              ETRACK, ETRACK - AM(JTRACK), ATRACK,
     &              SPAUSR(1),SPAUSR(2),SPAUSR(3),
     &              SPAUSR(5),SPAUSR(6),SPAUSR(7)
*     @@@                                                            @@@
      END IF
*     @@@                                                            @@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*
      RETURN
*
*======================================================================*
*                                                                      *
*     Event End DRAWing:                                               *
*                                                                      *
*======================================================================*
*                                                                      *
      ENTRY EEDRAW ( ICODE )
      RETURN
*
*======================================================================*
*                                                                      *
*     ENergy deposition DRAWing:                                       *
*                                                                      *
*     Icode = 1x: call from Kaskad                                     *
*             10: elastic interaction recoil                           *
*             11: inelastic interaction recoil                         *
*             12: stopping particle                                    *
*             13: pseudo-neutron deposition                            *
*             14: escape                                               *
*             15: time kill                                            *
*     Icode = 2x: call from Emfsco                                     *
*             20: local energy deposition (i.e. photoelectric)         *
*             21: below threshold, iarg=1                              *
*             22: below threshold, iarg=2                              *
*             23: escape                                               *
*             24: time kill                                            *
*     Icode = 3x: call from Kasneu                                     *
*             30: target recoil                                        *
*             31: below threshold                                      *
*             32: escape                                               *
*             33: time kill                                            *
*     Icode = 4x: call from Kashea                                     *
*             40: escape                                               *
*             41: time kill                                            *
*             42: delta ray stack overflow                             *
*     Icode = 5x: call from Kasoph                                     *
*             50: optical photon absorption                            *
*             51: escape                                               *
*             52: time kill                                            *
*                                                                      *
*======================================================================*
*                                                                      *
      ENTRY ENDRAW ( ICODE, MREG, RULL, XSCO, YSCO, ZSCO )
      RETURN
*
*======================================================================*
*                                                                      *
*     SOurce particle DRAWing:                                         *
*                                                                      *
*======================================================================*
*
      ENTRY SODRAW
*
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@                                                            @@@
      IF( LFIRST ) THEN
*
         NBGEVT = 0
         LFIRST = .FALSE.
*
      ENDIF
*     @@@                                                            @@@
      NBGEVT = NBGEVT + 1
*     @@@                                                            @@@
      DO 40 N  = 1, NPFLKA
*     @@@                                                            @@@
         ISPARK( 1, N ) = NBGEVT
*     @@@                                                            @@@
         SPAREK( 1, N ) = XFLK( N )
         SPAREK( 2, N ) = YFLK( N )
         SPAREK( 3, N ) = ZFLK( N )
*     @@@                                                            @@@
   40 CONTINUE
*     @@@                                                            @@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*     @@@@@@@@@@@                                            @@@@@@@@@@@
*
      RETURN
*
*======================================================================*
*                                                                      *
*     USer dependent DRAWing:                                          *
*                                                                      *
*     Icode = 10x: call from Kaskad                                    *
*             100: elastic   interaction secondaries                   *
*             101: inelastic interaction secondaries                   *
*             102: particle decay  secondaries                         *
*             103: delta ray  generation secondaries                   *
*             104: pair production secondaries                         *
*             105: bremsstrahlung  secondaries                         *
*             110: decay products                                      *
*     Icode = 20x: call from Emfsco                                    *
*             208: bremsstrahlung secondaries                          *
*             210: Moller secondaries                                  *
*             212: Bhabha secondaries                                  *
*             214: in-flight annihilation secondaries                  *
*             215: annihilation at rest   secondaries                  *
*             217: pair production        secondaries                  *
*             219: Compton scattering     secondaries                  *
*             221: photoelectric          secondaries                  *
*             225: Rayleigh scattering    secondaries                  *
*     Icode = 30x: call from Kasneu                                    *
*             300: interaction secondaries                             *
*     Icode = 40x: call from Kashea                                    *
*             400: delta ray  generation secondaries                   *
*  For all interactions secondaries are put on GENSTK common (kp=1,np) *
*  but for KASHEA delta ray generation where only the secondary elec-  *
*  tron is present and stacked on FLKSTK common for kp=npflka          *
*                                                                      *
*======================================================================*
*
      ENTRY USDRAW ( ICODE, MREG, XSCO, YSCO, ZSCO )
      RETURN
*=== End of subrutine Mgdraw ==========================================*
      END

