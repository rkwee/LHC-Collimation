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
*----------------------------------------------------------------------*
*                                                                      *
*     Elastic interaction sampling                                     *
*                                                                      *
*     Last change on 19-Oct-15     by   Francesco Cerutti              *
*                                                                      *
*----------------------------------------------------------------------*
*                                                                      *
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
      INCLUDE '(PART)'
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
      LOGICAL LFIRST
      SAVE LFIRST
      DATA LFIRST / .TRUE. /
*
      LOGICAL LSKPGD, LENOLD
*
      DIMENSION SUMINX (300)
*
      SAVE LSKPGD, SUMINX, TINLEN, SIGMCI, IEVENT, LASTMAT
      DATA LSKPGD / .TRUE. /
      DATA LASTMAT / -1 /
*
      NOMORE = 0
*  +-------------------------------------------------------------------*
*  |  First call initializations:
      IF ( LFIRST ) THEN
*  |  *** The following 3 cards are mandatory ***
         TKESUM = ZERZER
         LFIRST = .FALSE.
         LUSSRC = .TRUE.
*  |  *** User initialization ***
         WRITE (LUNOUT,*) 'Source routine forcing elastic interactions'
*      
         IEVENT = 0
         BEAWEI = ONEONE
      END IF
*  |
*  +-------------------------------------------------------------------*
      IEVENT = IEVENT + 1
*
      IJIJ   = IJBEAM
      POO    = PBEAM
      EKE    = SQRT ( PBEAM**2 + AM (IJBEAM)**2 ) - AM (IJBEAM)
      ELKE   = LOG (EKE)

      TXI = UBEAM
      TYI = VBEAM
      TZI = WBEAM
      XXX = XBEAM
      YYY = YBEAM
      ZZZ = ZBEAM

*  The following line makes the starting region search much more
*  robust if particles are starting very close to a boundary:
      CALL GEOCRS ( TXI, TYI, TZI )
      CALL GEOREG ( XXX, YYY, ZZZ, MREG, IDISC )
* 
*  For debugging: I get the material of the region where the particle is generated...
*     it should be VACUUM, of course...
      MMAT = MEDFLK(MREG,1)
*  +-------------------------------------------------------------------*
*  |  Interacting particle
*
*
      MMAT   = NINT(WHASOU(1))

      WEE    = BEAWEI
      BIAINE = ZERZER
      TXXPOL =-TWOTWO
      TYYPOL = ZERZER
      TZZPOL = ZERZER
*  +-------------------------------------------------------------------*
      IF (LASTMAT.NE.MMAT) THEN
        LASTMAT = MMAT
*  |  Compute the elastic sigma:
        LENOLD = .FALSE.
        SIGMCI = SGTELS ( IJIJ, EKE, ELKE, MMAT, LENOLD )
        WRITE (LUNOUT,*)' Elastic interaction cross section: ',
     &                               SIGMCI, ' (1/cm)'
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
               SUMINX (I) = CONTNT (I) * SGTELS ( IJIJ, EKE, ELKE,
     &                                            MMMAT, LENOLD )
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

*  Forcing the interaction
* 
      LEVFIN = .FALSE.   
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
      CALL NUCREL ( IJIJ, POO, EKE, TXI, TYI, TZI, TXXPOL, TYYPOL,
     &              TZZPOL, MMMAT, WEE)
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
      IF ( NP .NE. 1 ) THEN
         WRITE (LUNOUT,*)' SOURCE -- More than one particle, NP=',NP    
      END IF
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
     &        ILOFLK (NPFLKA) .LE. NALLWP ) THEN
            TKESUM = TKESUM + ( TKEFLK (NPFLKA)
     &           + AMDISC (ILOFLK(NPFLKA)) ) * WTFLK (NPFLKA)
         ELSE
            TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
         END IF

         IF( KPART(KP) .EQ. 1 ) THEN
            WRITE (92,*)' ',CXR(KP),' ',CYR(KP),' ',CZR(KP),' ',TKI(KP)   
         ENDIF
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
*=== End of subroutine Source =========================================*
*
102   FORMAT(4(1X,I4),7(1X,F18.8))
*
      END
      
