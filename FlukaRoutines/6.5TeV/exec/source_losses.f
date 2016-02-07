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
*     Created on 07 january 1990   by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*     Vasilis.Vlachoudis@cern.ch Jun 2004                              *
*                                                                      *
*     Special SOURCE routine for forcing interactions                  *
*                                                                      *
*     Reads a file with the coordinates of the inelastic scatterings   *
*     as produced by SixTrack                                          *
*     The filename is expected as BEAM card's SDUM                     *
*     (assumed as SDUM.dat)                                            *
*     Coordinate transformation is performed at inizialization level   *
*                                                                      *
*     The beam energy is defined with the BEAM card                    *
*     The beam direction is defined from the BEAMPOS card's SDUM       *
*     ( NEGATIVE -> beam 2)                                            *
*                                                                      *
*     SOURCE's WHAT(5) activates initialization check to spot          *
*     losses in vacuum                                                 *
*                                                                      *
*     SOURCE's WHAT(4)>0  unit number to dump original particle info   *
*                                                                      *
*     SOURCE's WHAT(2) inverts the X-axis (see comment below)          *
*                                                                      *
*                                                                      *
*     Last change on 26-Sep-14     by   Francesco Cerutti              *
*                                                                      *
*----------------------------------------------------------------------*
*
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
*
      INCLUDE '(EVTFLG)'
*
      INCLUDE 'COLSPE.inc'
*
      LOGICAL LFIRST, LSKPGD, LENOLD
*
      DIMENSION SUMINX (5000)
*
      SAVE LFIRST, LSKPGD, SUMINX, TINLEN, SIGMCI, IEVENT,
     &     LASTMAT, NVACUUM
      DATA LFIRST, LSKPGD / 2 * .TRUE. /
      DATA LASTMAT / -1 /
      DATA NVACUUM /  0 /
*
      PARAMETER (NINMAX=7800000)
*
      CHARACTER*250 LINE
      DIMENSION XIN(NINMAX), YIN(NINMAX), ZIN(NINMAX)
      DIMENSION UIN(NINMAX), VIN(NINMAX), WIN(NINMAX)
      SAVE NIN, XIN, YIN, ZIN, UIN, VIN, WIN

      NOMORE = 0
*  +-------------------------------------------------------------------*
*
* important setting in order to avoid problems with not reproducible 
* random sequences (still needed?)
*
      LEVFIN = .FALSE.
*
* _______________________________ INITIALIZATION START ________________*

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
*  |  |  Opening loss file
         ISP = INDEX(SDUSOU," ")-1
         IF (ISP.GT.0) THEN
            LINE = SDUSOU(1:INDEX(SDUSOU," ")-1)//".dat"
         ELSE
            LINE = SDUSOU//".dat"
         ENDIF
         WRITE (LUNOUT,*) 'Read source particles from '//LINE
         CALL OAUXFI(LINE,LUNRDB,'OLD',IERR)
         IF ( IERR .GT. 0 )
     &        CALL FLABRT('SOURCE','Error opening source file '//LINE)
* open SELected HISTories file on request to dump original particle info
         IF (NINT(WHASOU(4)) .GT. 0) 
     &        CALL OAUXFI('SEL_HIST',NINT(WHASOU(4)),'NEW',IERR)
         NIN = 0
* Normal loading of losses (collimator sampling not implemented)
 10      CONTINUE
         READ( LUNRDB, '(A)', ERR=9999, END=20 ) LINE
         IF ( LINE(1:1) .EQ. '#' ) GO TO 10
* collimator index, rotation [rad], loss z [m], x [mm], x' ["mrad"],
* y [mm], y' ["mrad"], unused integers
* actually x' and y' are the tangent, not the angle
         READ (LINE,*) ICOLIN,COLROT,ZFFF,XSITR,XPSITR,YSITR,YPSITR,
     &        INTYPE,IPARIDE,ITURN
*
* neglect loss on a collimator not in the geometry 
* (or closed, on the other beam)
         IF(ITRACL(ICOLIN).EQ.-1) GO TO 10

         NIN = NIN + 1
         IF (NIN.GT.NINMAX) CALL FLABRT('SOURCE','Increase NINMAX')
* ZFFF=0 corresponds to the jaw upstream face
* (according to the beam direction)
         ZHELP=(ZFFF-COLLEN(ICOLIN)/TWOTWO)*1.D+02
         XHELP=XSITR/TENTEN
         XPHELP=XPSITR/1.D+03
         YHELP=YSITR/TENTEN
         YPHELP=YPSITR/1.D+03
         DIRNOR=SQRT(ONEONE+XPHELP**2+YPHELP**2)
         XPHELP=XPHELP/DIRNOR
         YPHELP=YPHELP/DIRNOR
         ZPHELP=ONEONE/DIRNOR

* Beam 2 (selected through NEGATIVE in BEAMPOS card): further pi rotation
* However, pay attention! If the collimator transformation already includes
* a further pi rotation (as for Lefteris' assemblies), NEGATIVE must not be
* used, in order to prevent a double rotation 
         IF (WBEAM.LT.ZERZER) THEN
            ZHELP = -ZHELP
            XHELP = -XHELP
            XPHELP = -XPHELP
            ZPHELP = -ZPHELP
         END IF 

* Activate inversion of X-axis. This could be requested in case the collimator
* losses are produced for one beam and then applied in FLUKA to the other beam.
* However, pay attention! There is no clear consensus on the need of this 
* inversion
         IF (ABS(WHASOU(2)).GT.ANGLGB) THEN
            XHELP = -XHELP
            XPHELP = -XPHELP
         END IF 

         NPOINT=1
         CALL UNDOTR ( NPOINT, XHELP, YHELP, ZHELP, ITRACL(ICOLIN) )
         XIN(NIN)=XHELP
         YIN(NIN)=YHELP
         ZIN(NIN)=ZHELP
         CALL UNDRTO (NPOINT, XPHELP, YPHELP, ZPHELP, ITRACL(ICOLIN))
         UIN(NIN)=XPHELP
         VIN(NIN)=YPHELP
         WIN(NIN)=ZPHELP

* Check on request if material is vacuum
         IF (ABS(WHASOU(5)).GT.ANGLGB) THEN
            CALL GEOCRS ( XPHELP, YPHELP, ZPHELP )
            CALL GEOREG ( XHELP, YHELP, ZHELP, MREG, IDISC )
            MMAT = MEDFLK(MREG,1)
            IF (MMAT.EQ.2) THEN
               WRITE(LUNERR,*) "**************************************"
               WRITE(LUNERR,*) "ERROR in source.f: N=",NIN,
     &              " File Pos=", XSITR, YSITR, ZFFF,
     &              " Geo  Pos=", XHELP,YHELP,ZHELP
               WRITE(LUNERR,*) " REG=",MREG
               WRITE(LUNOUT,*) "ERROR in source.f: N=",NIN,
     &              " File Pos=", XSITR, YSITR, ZFFF,
     &              " Geo  Pos=", XHELP,YHELP,ZHELP
               WRITE(LUNOUT,*) " REG=",MREG
            END IF
         END IF
         GOTO 10
 20      CONTINUE
         WRITE (LUNOUT,*) NIN,' particles loaded'
         WRITE (LUNOUT,*) "-------------------------------------"
         CLOSE(UNIT=LUNRDB)

         IEVENT = 0
         BEAWEI = ONEONE
      END IF
*  |
* _______________________________ INITIALIZATION END ___________________

      IEVENT = IEVENT + 1

*  | Choose a random particle
* Normal choice of the particle in the full event list
      RNDSIG1 = FLRNDM (RNDSIG1)
      N = INT(NIN*RNDSIG1)+1

*  it should never happen
      IF (N.GT.NIN) N=NIN

      IJIJ   = IJBEAM

* Cosines (tx,ty,tz)
      TXI    = UIN(N)
      TYI    = VIN(N)
      TZI    = WIN(N)
* Particle coordinates
      XXX    = XIN(N)
      YYY    = YIN(N)
      ZZZ    = ZIN(N)

      POO    = PBEAM
      EKE    = SQRT ( PBEAM**2 + AM (IJBEAM)**2 ) - AM (IJBEAM)
      ELKE   = LOG (EKE)

      CALL GEOCRS ( TXI, TYI, TZI )
      CALL GEOREG ( XXX, YYY, ZZZ, MREG, IDISC )
  
      MMAT   = MEDFLK(MREG,1)
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
         WRITE(LUNERR,*) "N=",N," POS=",XXX,YYY,ZZZ,
     &        " DIR=",TXI,TYI,TZI," REG=",MREG," MAT=",MMAT
         WRITE(LUNERR,*) "     Material is VACUUM replaced by CARBON"
         WRITE(LUNOUT,*) "     Material is VACUUM replaced by CARBON"
         MMAT = 6
* 
         IF (NVACUUM.GT.500) STOP 'TOO MANY INTERACTIONS IN VACUUM'
      ELSE IF (MMAT.EQ.1) THEN
         CALL FLABRT('SOURCE','INTERACTION IN BLACKHOLE')
      ENDIF

* mb /
*  +-------------------------------------------------------------------*
*  |  Dump on request source particle information
      IF (NINT(WHASOU(4)) .GT. 0) THEN
         WRITE(NINT(WHASOU(4)),102) MLATTC, IJIJ, MREG, MMAT, EKE, XXX,
     &        YYY, ZZZ, TXI, TYI, TZI
         CALL FLUSH(NINT(WHASOU(4)))
      END IF

      IF (LASTMAT.NE.MMAT) THEN
         LASTMAT = MMAT
*  |  Compute the inelastic sigma:
         LENOLD = .FALSE.
         SIGMCI = SGTINL ( IJIJ, EKE, ELKE, MMAT, LENOLD )
         WRITE (LUNOUT,*)' *** Beam interaction cross section: ',
     &        SIGMCI, ' (1/cm)'
*  |  +----------------------------------------------------------------*
*  |  |  If it is a compound compute the partial xsec
*  |  |  Compound:
         IF ( ICOMP (MMAT) .GT. 0 ) THEN
            TINLEN = ZERZER
*  |  |  +-------------------------------------------------------------*
*  |  |  |  Loop on constituents:
            DO 1000 I = ICOMP (MMAT), ICOMP (MMAT) + ICOMPL (MMAT) - 1
               MMMAT = MATNUM (I)
               LENOLD = .FALSE.
               SUMINX (I) = CONTNT (I) * SGTINL ( IJIJ, EKE, ELKE,
     &              MMMAT, LENOLD )
     &              / RHO (MMMAT)
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
         I = I - 1
 2500    CONTINUE
         MMMAT = MATNUM (I)
      END IF

*  Perform the inelastic interaction of the original particle
*  in the respective material
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
*  +-------------------------------------------------------------------*
*  Skip this part, it could cause problems if in vacuum:
      IF ( LSKPGD ) GO TO 9000
      UVVU    = WEE * TVBIND
      EDPSCO (10, 1)= EDPSCO (10, 1) + UVVU
      UVVU23  = WEE * TVCMS
      EDPSCO (7, 1) = EDPSCO (7, 1) + UVVU23
*  Score evaporated d, 3-H, 3-He, 4-He in the secondary budget:
      WEPRDC (-3, 1) = WEPRDC (-3, 1) + WEE * IEVDEU
      WEPRDC (-4, 1) = WEPRDC (-4, 1) + WEE * IEVTRI
      WEPRDC (-5, 1) = WEPRDC (-5, 1) + WEE * IEV3HE
      WEPRDC (-6, 1) = WEPRDC (-6, 1) + WEE * IEV4HE
      UVVU13  = WEE * ( TVRECL  + TVHEAV )
      EDPSCO (3, 1) = EDPSCO (3, 1) + UVVU13
      UVVU    = UVVU13  + UVVU23
      LLO     = 1
      MTRACK  = 0
      NTRACK  = 0
      WTRACK  = WEE
      LT1TRK  = MLATTC
      LT2TRK  = MLATTC
      WSCRNG  = WEE
      IF ( UVVU .GT. AZRZRZ )
     &   CALL GEODEN ( 208, XXX, YYY, ZZZ, MREG, UVVU, 4030, LLO,
     &                 UVVU, 0)
 9000 CONTINUE
      TV      = ZERZER
      TVCMS   = ZERZER
      TVRECL  = ZERZER
      TVHEAV  = ZERZER
      TVBIND  = ZERZER
      RETURN
 9999 CONTINUE
      STOP "ERROR Opening source file"
*=== End of subroutine Source =========================================*
*
102   FORMAT(4(1X,I4),7(1X,F18.8))
*
      END
