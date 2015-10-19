*$ CREATE SOURCE.FOR
*COPY SOURCE
*
*=== source ===========================================================*
*
      SUBROUTINE SOURCE ( NOMORE )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1990-2010      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*                                                                      *
*     New source for FLUKA9x-FLUKA20xy:                                *
*                                                                      *
*     Created on 07 January 1990   by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*     Last change on  17-Oct-10    by    Alfredo Ferrari               *
*                                                                      *
*  This is just an example of a possible user written source routine.  *
*  note that the beam card still has some meaning - in the scoring the *
*  maximum momentum used in deciding the binning is taken from the     *
*  beam momentum.  Other beam card parameters are obsolete.            *
*                                                                      *
*       Output variables:                                              *
*                                                                      *
*              Nomore = if > 0 the run will be terminated              *
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
*

      DIMENSION SUMINX (300)
      LOGICAL LFIRST
      INTEGER npindex
*
      SAVE LFIRST
      SAVE npindex
      DATA LFIRST / .TRUE. /

      PARAMETER (NINMAX=3500000)

      CHARACTER*250 LINE
      DIMENSION XIN(NINMAX), YIN(NINMAX), ZIN(NINMAX)
      DIMENSION UIN(NINMAX), VIN(NINMAX)
      SAVE NIN, XIN, YIN, ZIN, UIN, VIN
*

*======================================================================*
*                                                                      *
*                 BASIC VERSION                                        *
*                                                                      *
*======================================================================*
      NOMORE = 0
*  +-------------------------------------------------------------------*
*  |  First call initializations:
      IF ( LFIRST ) THEN
*  |  *** The following 3 cards are mandatory ***
         TKESUM = ZERZER
         LFIRST = .FALSE.
         LUSSRC = .TRUE.
*  |  *** User initialization ***
         npindex=0
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
*  Push one source particle to the stack. Note that you could as well
*  push many but this way we reserve a maximum amount of space in the
*  stack for the secondaries to be generated
*  Npflka is the stack counter: of course any time source is called it
*  must be =0
      NPFLKA = NPFLKA + 1
*  Wt is the weight of the particle
      WTFLK  (NPFLKA) = ONEONE
      WEIPRI = WEIPRI + WTFLK (NPFLKA)
*  Particle type (1=proton.....). Ijbeam is the type set by the BEAM
*  card
*  +-------------------------------------------------------------------*
*  |  (Radioactive) isotope:
      IF ( IJBEAM .EQ. -2 .AND. LRDBEA ) THEN
         IARES  = IPROA
         IZRES  = IPROZ
         IISRES = IPROM
         CALL STISBM ( IARES, IZRES, IISRES )
         IJHION = IPROZ  * 1000 + IPROA
         IJHION = IJHION * 100 + KXHEAV
         IONID  = IJHION
         CALL DCDION ( IONID )
         CALL SETION ( IONID )
*  |
*  +-------------------------------------------------------------------*
*  |  Heavy ion:
      ELSE IF ( IJBEAM .EQ. -2 ) THEN
         IJHION = IPROZ  * 1000 + IPROA
         IJHION = IJHION * 100 + KXHEAV
         IONID  = IJHION
         CALL DCDION ( IONID )
         CALL SETION ( IONID )
         ILOFLK (NPFLKA) = IJHION
*  |  Flag this is prompt radiation
         LRADDC (NPFLKA) = .FALSE.
*  |  Group number for "low" energy neutrons, set to 0 anyway
         IGROUP (NPFLKA) = 0
*  |
*  +-------------------------------------------------------------------*
*  |  Normal hadron:
      ELSE
         IONID = IJBEAM
         ILOFLK (NPFLKA) = IJBEAM
*  |  Flag this is prompt radiation
         LRADDC (NPFLKA) = .FALSE.
*  |  Group number for "low" energy neutrons, set to 0 anyway
         IGROUP (NPFLKA) = 0
      END IF
*  |
*  +-------------------------------------------------------------------*
*  From this point .....
*  Particle generation (1 for primaries)
      LOFLK  (NPFLKA) = 1
*  User dependent flag:
      LOUSE  (NPFLKA) = 0
*  No channeling:
      LCHFLK (NPFLKA) = .FALSE.
      DCHFLK (NPFLKA) = ZERZER
*  User dependent spare variables:
      DO 100 ISPR = 1, MKBMX1
         SPAREK (ISPR,NPFLKA) = ZERZER
 100  CONTINUE
*  User dependent spare flags:
      DO 200 ISPR = 1, MKBMX2
         ISPARK (ISPR,NPFLKA) = 0
 200  CONTINUE
*  Save the track number of the stack particle:
      ISPARK (MKBMX2,NPFLKA) = NPFLKA
      NPARMA = NPARMA + 1
      NUMPAR (NPFLKA) = NPARMA
      NEVENT (NPFLKA) = 0
      DFNEAR (NPFLKA) = +ZERZER
*  ... to this point: don't change anything
*  Particle age (s)
      AGESTK (NPFLKA) = +ZERZER
      AKNSHR (NPFLKA) = -TWOTWO
*  Kinetic energy of the particle (GeV)
      TKEFLK (NPFLKA) = SQRT ( PBEAM**2 + AM (IONID)**2 ) - AM (IONID)
*  Particle momentum
      PMOFLK (NPFLKA) = PBEAM
*     PMOFLK (NPFLKA) = SQRT ( TKEFLK (NPFLKA) * ( TKEFLK (NPFLKA)
*    &                       + TWOTWO * AM (IONID) ) )


*********************************
* now select particle from file
      npindex=npindex+1
      N=npindex

* Cosines
c$$$      DCX=TAN(UIN(N))
c$$$      DCY=TAN(VIN(N))
      DCX=UIN(N)
      DCY=VIN(N)
*      FNORM = SQRT(DCX**2+DCY**2+ONEONE)
      FNORM=ONEONE
      TXI    = DCX / FNORM
      TYI    = DCY / FNORM
      TZI    = SQRT ( ONEONE - TXI**2 - TYI**2 )
      IF (WBEAM.LT.ZERZER) TZI = -TZI
* Particle coordinates
      XXX    = XIN(N)
      YYY    = YIN(N)
      ZZZ    = ZIN(N)
     
* save coordinates of initial particle in common block
      xStart=XXX
      yStart=YYY
      zStart=ZZZ
      tStart=tIn(N)
      runNr=WHASOU(1)

continue standard source with modifications
**************************

*  Cosines (tx,ty,tz)
      TXFLK  (NPFLKA) = TXI
      TYFLK  (NPFLKA) = TYI
      TZFLK  (NPFLKA) = TZI
*      TZFLK  (NPFLKA) = WBEAM
*      TZFLK  (NPFLKA) = SQRT ( ONEONE - TXFLK (NPFLKA)**2
*     &                       - TYFLK (NPFLKA)**2 )
*  Polarization cosines:
      TXPOL  (NPFLKA) = -TWOTWO
      TYPOL  (NPFLKA) = +ZERZER
      TZPOL  (NPFLKA) = +ZERZER
*  Particle coordinates
      XFLK   (NPFLKA) = XXX
      YFLK   (NPFLKA) = YYY
      ZFLK   (NPFLKA) = ZZZ

*  dump coordinates for debugging
      write(88,*) TXFLK  (NPFLKA),TYFLK  (NPFLKA),TZFLK  (NPFLKA),
     &     XFLK(NPFLKA),YFLK(NPFLKA),ZFLK(NPFLKA)
*  Calculate the total kinetic energy of the primaries: don't change
      IF ( ILOFLK (NPFLKA) .EQ. -2 .OR. ILOFLK (NPFLKA) .GT. 100000 )
     &   THEN
         TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
      ELSE IF ( ILOFLK (NPFLKA) .NE. 0 ) THEN
         TKESUM = TKESUM + ( TKEFLK (NPFLKA) + AMDISC (ILOFLK(NPFLKA)) )
     &          * WTFLK (NPFLKA)
      ELSE
         TKESUM = TKESUM + TKEFLK (NPFLKA) * WTFLK (NPFLKA)
      END IF
      RADDLY (NPFLKA) = ZERZER
*  Here we ask for the region number of the hitting point.
*     NREG (NPFLKA) = ...
*  The following line makes the starting region search much more
*  robust if particles are starting very close to a boundary:
      CALL GEOCRS ( TXFLK (NPFLKA), TYFLK (NPFLKA), TZFLK (NPFLKA) )
      CALL GEOREG ( XFLK  (NPFLKA), YFLK  (NPFLKA), ZFLK  (NPFLKA),
     &              NRGFLK(NPFLKA), IDISC )
*  Do not change these cards:
      CALL GEOHSM ( NHSPNT (NPFLKA), 1, -11, MLATTC )
      NLATTC (NPFLKA) = MLATTC
      CMPATH (NPFLKA) = ZERZER
      CALL SOEVSV
      RETURN
 9999 CONTINUE
      STOP "ERROR reading loss file" 
*=== End of subroutine Source =========================================*
      END

