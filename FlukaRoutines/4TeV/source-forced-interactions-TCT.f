*$ CREATE SOURCE.FOR
*COPY SOURCE
*
*=== source ===========================================================*
*
      SUBROUTINE SOURCE (NOMORE)

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1990-2009      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*     Created on 07 january 1990   by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*----------------------------------------------------------------------*
*                                                                      *
*     Special SOURCE routine for forcing inelastic interactions        *
*                                                                      *
*     Vasilis.Vlachoudis@cern.ch Jun 2004                              *
*                                                                      *
*                                          &  CERN FLUKA team          *
*                                                                      *
*     It reads a file with the coordinates of inelastic scatterings    *
*     The filename is SDUM.dat with SDUM input in the SOURCE card      *
*     The file should contain x y z [in cm] x' y' [angles in rad]      *
*     The beam particle energy is defined with the BEAM card           *
*     The beam particle direction along z is defined from the SDUM     *
*                                                  in the BEAMPOS card *
*                                                                      *
*     Cleaned on 28-apr-10     by    Francesco Cerutti                 *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE 'include_IR1IR5.f'


      INCLUDE '(BEAMCM)'
      INCLUDE '(CASLIM)'
      INCLUDE '(COMPUT)'
      INCLUDE '(CTITLE)'
      INCLUDE '(SOURCM)'
      INCLUDE '(FHEAVY)'
      INCLUDE '(GENSTK)'
      INCLUDE '(LTCLCM)'
      INCLUDE '(FLKMAT)'
      INCLUDE '(MULBOU)'
      INCLUDE '(PAPROP)'
      INCLUDE '(PAREVT)'
      INCLUDE '(PARNUC)'
      INCLUDE '(RESNUC)'
      INCLUDE '(SNNUCM)'
      INCLUDE '(FLKSTK)'
      INCLUDE '(SUMCOU)'
      INCLUDE '(TRACKR)'
      INCLUDE '(USRBIN)'
      INCLUDE '(FLKCMP)'
      INCLUDE '(EVTFLG)'

      LOGICAL LFIRST
*
      DIMENSION SUMINX (300)
*
      SAVE LFIRST, SUMINX, TINLEN, SIGMCI, LASTMAT, NVACUUM
      DATA LFIRST / .TRUE. /
      DATA LASTMAT / -1 /
*
      PARAMETER (NINMAX=3500000)
*
      CHARACTER*250 LINE
      DIMENSION XIN(NINMAX), YIN(NINMAX), ZIN(NINMAX)
      DIMENSION UIN(NINMAX), VIN(NINMAX)
      SAVE NIN, XIN, YIN, ZIN, UIN, VIN
*
      NOMORE = 0
*  +-------------------------------------------------------------------*
*
* important setting in order to avoid problems with not reproducible 
* random sequences! [may be now pleonastic]
      LEVFIN = .FALSE.
*
* _________________________ INITIALIZATION START ______________________      
*
*  +-------------------------------------------------------------------*
*  |  First call initializations:
      IF ( LFIRST ) THEN
*  |  *** The following 3 cards are mandatory ***
         TKESUM = ZERZER
         LFIRST = .FALSE.
         LUSSRC = .TRUE.
*  |  *** User initialization ***
*
*  |  +----------------------------------------------------------------*
*  |  |  Load file given on SDUM of the SOURCE card
         ISP = INDEX(SDUSOU," ")-1
         IF (ISP.GT.0) THEN
           LINE = SDUSOU(1:INDEX(SDUSOU," ")-1)//".dat"
         ELSE
           LINE = SDUSOU//".dat"
         ENDIF
         WRITE (LUNOUT,*) 'Read source particles from '//LINE
         CALL OAUXFI(LINE,LUNRDB,'OLD',IERR)
         IF ( IERR .GT. 0 )
     +       CALL FLABRT('SOURCE','Error opening loss file '//LINE)
         NIN = 0
* Normal loading of losses (collimator sampling not activated)
10       CONTINUE
           READ( LUNRDB, '(A)', ERR=9999, END=20 ) LINE
           IF ( LINE(1:1) .EQ. '#' ) GO TO 10
           NIN = NIN + 1
           IF (NIN.GT.NINMAX) CALL FLABRT('SOURCE','Increase NINMAX')
           READ (LINE,*) XIN(NIN), YIN(NIN), ZIN(NIN),
     +                     UIN(NIN), VIN(NIN),tIn(NIN)
           GOTO 10
20       CONTINUE
         WRITE (LUNOUT,*) NIN,' particles loaded'
         WRITE (LUNOUT,*) "-------------------------------------"
         CLOSE(UNIT=LUNRDB)
*  |  |
*  |  +----------------------------------------------------------------*
*
         BEAWEI = ONEONE
      END IF
*  |
*  +-------------------------------------------------------------------*
* _______________________________ INITIALIZATION END ___________________      

*
*  | Choose a random particle
* Normal choice of the particle in the full events list        
      RNDSIG1 = FLRNDM (RNDSIG1)
      N = INT(NIN*RNDSIG1)+1

      IF (N.GT.NIN) N=NIN ! it should never happen

      IJIJ   = IJBEAM

* Cosines
      DCX=TAN(UIN(N))
      DCY=TAN(VIN(N))
      FNORM = SQRT(DCX**2+DCY**2+ONEONE)
      TXI    = DCX / FNORM
      TYI    = DCY / FNORM
      TZI    = SQRT ( ONEONE - TXI**2 - TYI**2 )
      IF (WBEAM.LT.ZERZER) TZI = -TZI
* Particle coordinates
      XXX    = XIN(N)
      YYY    = YIN(N)
      ZZZ    = ZIN(N)

c$$$      XXX = 0.d0
c$$$      YYY=0.d0
c$$$      ZZZ=2262.d0
c$$$      TXI=0.d0
c$$$      TYI=0.d0
c$$$      TZI    = SQRT ( ONEONE - TXI**2 - TYI**2 )
c$$$      IF (WBEAM.LT.ZERZER) TZI = -TZI
     
* save coordinates of initial particle in common block
      xStart=XXX
      yStart=YYY
      zStart=ZZZ
      tStart=tIn(N)
      runNr=WHASOU(1)

      write(88,*) XXX,YYY,ZZZ,tStart
*      write(88,*) WHASOU(1) 

      POO    = PBEAM
      EKE    = SQRT ( PBEAM**2 + AM (IJBEAM)**2 ) - AM (IJBEAM)
      ELKE   = LOG (EKE)

*  The following line makes the starting region search much more
*  robust if particles are starting very close to a boundary:
      CALL GEOCRS ( TXI, TYI, TZI )
      CALL GEOREG ( XXX, YYY, ZZZ, MREG, IDISC )
        
      MMAT   = MEDFLK(MREG,1)
*      MMAT   = MEDIUM(MREG)
*      MMAT = 23
      WEE    = BEAWEI
      BIAINE = ZERZER
      TXXPOL =-TWOTWO
      TYYPOL = ZERZER     
      TZZPOL = ZERZER

      IF (MMAT.EQ.2) THEN
        NVACUUM = NVACUUM + 1
        WRITE(LUNERR,*) "*******************************************"
        WRITE(LUNERR,*) "ERROR in source.f: On position=",XXX,YYY,ZZZ
        WRITE(LUNOUT,*) "ERROR in source.f: On position=",XXX,YYY,ZZZ
        WRITE(LUNERR,*) "loss point N=",N,
     +                  " DIR=",TXI,TYI,TZI," REG=",MREG
        WRITE(LUNERR,*) "     Material is VACUUM replaced by TUNGSTEN"
        WRITE(LUNOUT,*) "     Material is VACUUM replaced by TUNGSTEN"
        MMAT = 23
* 
        IF (NVACUUM.GT.20) STOP 'TOO MANY INTERACTIONS IN VACUUM'
      ENDIF

c possible debugging dump
c      print *, MLATTC, IJIJ, MREG, MMAT, EKE, XXX,
c     +                YYY, ZZZ, TXI, TYI, TZI
            
      IF (LASTMAT.NE.MMAT) THEN
          LASTMAT = MMAT
*  |  Compute the inelastic sigma:
         SIGMCI = SGTINL ( IJIJ, EKE, ELKE, MMAT, .FALSE. )
         WRITE (LUNOUT,*)' *** Beam interaction cross section: ',
     &                         SIGMCI, ' (1/cm)  in material # ',MMAT
*  |  +----------------------------------------------------------------*
*  |  |  If it is a compound compute the partial xsec
*  |  |  Compound:
         IF ( ICOMP (MMAT) .GT. 0 ) THEN
            TINLEN = ZERZER
*  |  |  +-------------------------------------------------------------*
*  |  |  |  Loop on constituents:
            DO 1000 I = ICOMP (MMAT), ICOMP (MMAT) + ICOMPL (MMAT) - 1
               MMMAT = MATNUM (I)
               SUMINX (I) = CONTNT (I) * SGTINL ( IJIJ, EKE, ELKE,
     &                                            MMMAT, .FALSE. )
     &                    / RHO (MMMAT)
               SUMINX (I) = SUMINX (I) + TINLEN
               TINLEN = SUMINX (I)
 1000       CONTINUE
*  |  |  |
*  |  |  +-------------------------------------------------------------*
         END IF
*  |  |
*  |  +----------------------------------------------------------------*
      ENDIF
*  |
*  +-------------------------------------------------------------------*

*  +-------------------------------------------------------------------*
*  |  Elements:
      IF ( ICOMP (MMAT) .LE. 0 ) THEN
         MMMAT = MMAT
*  |
*  +-------------------------------------------------------------------*
*  |  Compounds:
      ELSE
         RCONT = TINLEN * FLRNDM (RCONT)
         DO 2000 I = ICOMP (MMAT), ICOMP (MMAT) + ICOMPL (MMAT) - 1
            IF ( RCONT .LE. SUMINX (I) ) GO TO 2500
 2000    CONTINUE
         I = I - 1 ! it should never happen
 2500    CONTINUE
         MMMAT = MATNUM (I)
      END IF
      CALL EVENTX ( IJIJ, POO, EKE, TXI, TYI, TZI, TXXPOL, TYYPOL,
     &              TZZPOL, WEE, MMMAT, BIAINE )
*  |
*  +-------------------------------------------------------------------*
*  Load on stack (temporarily for Soevsv) the incoming projectile:
      NPFLKA = 1
      XFLK   (NPFLKA) = XXX
      YFLK   (NPFLKA) = YYY
      ZFLK   (NPFLKA) = ZZZ
      TXFLK  (NPFLKA) = TXI
      TYFLK  (NPFLKA) = TYI
      TZFLK  (NPFLKA) = TZI
      TXPOL  (NPFLKA) =-TWOTWO
      TYPOL  (NPFLKA) = ZERZER
      TZPOL  (NPFLKA) = ZERZER
      WTFLK  (NPFLKA) = WEE
      TKEFLK (NPFLKA) = ZERZER
      PMOFLK (NPFLKA) = ZERZER
      ILOFLK (NPFLKA) = IJBEAM
      NRGFLK (NPFLKA) = MREG
      NLATTC (NPFLKA) = MLATTC
      AGESTK (NPFLKA) = ZERZER
      AKNSHR (NPFLKA) =-TWOTWO
      WEIPRI = WEIPRI + WTFLK (NPFLKA)
*  +-------------------------------------------------------------------*

      CALL SOEVSV
      NPFLKA = 0

*  +-------------------------------------------------------------------*
*  |  Lstack is the stack counter: of course any time source is called
*  |  it must be =0
      DO 4000 KP = 1, NP
         NPFLKA = NPFLKA + 1
*  |  Wt is the weight of the particle
         WTFLK  (NPFLKA) = WEI   (KP)
         ILOFLK (NPFLKA) = KPART (KP)
         LOFLK  (NPFLKA) = 1
         NPARMA          = NPARMA + 1
         NUMPAR (NPFLKA) = NPARMA
         NEVENT (NPFLKA) = 0
*  |  User dependent flag:
         LOUSE  (NPFLKA) = 0
*  |  User dependent spare variables:
         DO 3600 ISPR = 1, MKBMX1
            SPAREK (ISPR,NPFLKA) = ZERZER
 3600    CONTINUE
*  |  User dependent spare flags:
         DO 3800 ISPR = 1, MKBMX2
            ISPARK (ISPR,NPFLKA) = 0
 3800    CONTINUE
*  |  Save the track number of the stack particle:
         ISPARK (MKBMX2,NPFLKA) = NPFLKA
         DFNEAR (NPFLKA) = +ZERZER
         AGESTK (NPFLKA) = +ZERZER
         AKNSHR (NPFLKA) = -TWOTWO
         IGROUP (NPFLKA) = 0
         TKEFLK (NPFLKA) = TKI (KP)
*  |  Particle momentum
         PMOFLK (NPFLKA) = PLR (KP)
*  |  Cosines (tx,ty,tz)
         TXFLK  (NPFLKA) = CXR (KP)
         TYFLK  (NPFLKA) = CYR (KP)
         TZFLK  (NPFLKA) = CZR (KP)
*  |  Polarization cosines:
         TXPOL  (NPFLKA) = CXRPOL (KP)
         TYPOL  (NPFLKA) = CYRPOL (KP)
         TZPOL  (NPFLKA) = CZRPOL (KP)
         CXRPOL (KP) = - TWOTWO
         CYRPOL (KP) = + ZERZER
         CZRPOL (KP) = + ZERZER
         XFLK   (NPFLKA) = XXX
         YFLK   (NPFLKA) = YYY
         ZFLK   (NPFLKA) = ZZZ
         NRGFLK (NPFLKA) = MREG
         NLATTC (NPFLKA) = MLATTC
*  |  Calculate the total kinetic energy of the primaries: don't change
         IF ( ILOFLK (NPFLKA) .NE. 0 .AND.
     &           ILOFLK (NPFLKA) .LE. NALLWP ) THEN
            TKESUM = TKESUM + ( TKEFLK (NPFLKA)
     &             + AMDISC (ILOFLK(NPFLKA)) ) * WTFLK (NPFLKA)
         ELSE
            TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
         END IF
 4000 CONTINUE
*  |
*  +-------------------------------------------------------------------*
      NP  = 0
      NP0 = 0
*  +-------------------------------------------------------------------*
*  | "Heavy" transport requested:
      IF ( LHEAVY ) THEN
*  |  +----------------------------------------------------------------*
*  |  |  Lstack is the stack counter: of course any time source is
*  |  |  called it must be =0
         DO 5000 KP = 1, NPHEAV
            NPFLKA = NPFLKA + 1
*  |  |  Wt is the weight of the particle
            WTFLK  (NPFLKA) = WHEAVY (KP)
            ILOFLK (NPFLKA) =-KHEAVY (KP)
            LOFLK  (NPFLKA) = 1
            NPARMA          = NPARMA + 1
            NUMPAR (NPFLKA) = NPARMA
            NEVENT (NPFLKA) = 0
*  |  |  User dependent flag:
            LOUSE  (NPFLKA) = 0
*  |  |  User dependent spare variables:
            DO 4600 ISPR = 1, MKBMX1
               SPAREK (ISPR,NPFLKA) = ZERZER
 4600        CONTINUE
*  |  |  User dependent spare flags:
            DO 4800 ISPR = 1, MKBMX2
               ISPARK (ISPR,NPFLKA) = 0
 4800        CONTINUE
*  |  |  Save the track number of the stack particle:
            ISPARK (MKBMX2,NPFLKA) = NPFLKA
            DFNEAR (NPFLKA) = +ZERZER
            AGESTK (NPFLKA) = +ZERZER
            AKNSHR (NPFLKA) = -TWOTWO
            IGROUP (NPFLKA) = 0
            TKEFLK (NPFLKA) = TKHEAV (KP)
*  |  |  Particle momentum
            PMOFLK (NPFLKA) = PHEAVY (KP)
*  |  |  Cosines (tx,ty,tz)
            TXFLK  (NPFLKA) = CXR (KP)
            TYFLK  (NPFLKA) = CYR (KP)
            TZFLK  (NPFLKA) = CZR (KP)
*  |  |  Polarization cosines:
            TXPOL  (NPFLKA) = - TWOTWO
            TYPOL  (NPFLKA) = + ZERZER
            TZPOL  (NPFLKA) = + ZERZER
*  |  |  Particle coordinates
            XFLK   (NPFLKA) = XXX
            YFLK   (NPFLKA) = YYY
            ZFLK   (NPFLKA) = ZZZ
            NRGFLK (NPFLKA) = MREG
*  |  |  Do not change this card:
            NLATTC (NPFLKA) = MLATTC
*  |  |  Calculate the total kinetic energy of the primaries: don't
*  |  |  change
            TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
 5000    CONTINUE
*  |  |
*  |  +----------------------------------------------------------------*
         TVHEAV = ZERZER
         NPHEAV = 0
      END IF
*  |
      TV      = ZERZER
      TVCMS   = ZERZER
      TVRECL  = ZERZER
      TVHEAV  = ZERZER
      TVBIND  = ZERZER
      RETURN
 9999 CONTINUE
      STOP "ERROR reading loss file"
*=== End of subroutine Source =========================================*
      END
