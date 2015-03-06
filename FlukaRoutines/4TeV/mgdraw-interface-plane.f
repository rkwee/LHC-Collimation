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

      INCLUDE 'include_IR1IR5.f'
*
      DIMENSION DTQUEN ( MXTRCK, MAXQMG )
*
      CHARACTER*20 FILNAM

      LOGICAL LFCOPE
      SAVE LFCOPE
      DATA LFCOPE / .FALSE. /

      LOGICAL LFIRST
      DATA LFIRST / .TRUE. /
      SAVE LFIRST
*      
      SAVE IREGSTART
      SAVE IREGEND

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


      IF ( LFIRST ) THEN
         write(lunout,*)'I am using FLUSCW for LATTICE debugging'
         LFIRST = .FALSE.
* Get and save the region numbers
         CALL GEON2R("SCREG01 ",IREGSTART,IERR1)
         CALL GEON2R("SCREG02 ",IREGEND,IERR2)
      ENDIF

      IF(IERR1 .NE. 0 .OR. IERR2 .NE. 0) STOP "Error in name conversion"

      IF ( .NOT. LFCOPE ) THEN
         LFCOPE = .TRUE.
         IF ( KOMPUT .EQ. 2 ) THEN
            FILNAM = '/'//CFDRAW(1:8)//' DUMP A'
         ELSE
            FILNAM = CFDRAW
         END IF
c$$$         OPEN ( UNIT = IODRAW, FILE = FILNAM, STATUS = 'NEW', FORM =
c$$$     &          'UNFORMATTED' )
      END IF
c$$$      WRITE (IODRAW) NTRACK, MTRACK, JTRACK, SNGL (ETRACK),
c$$$     &               SNGL (WTRACK)
c$$$      WRITE (IODRAW) ( SNGL (XTRACK (I)), SNGL (YTRACK (I)),
c$$$     &                 SNGL (ZTRACK (I)), I = 0, NTRACK ),
c$$$     &               ( SNGL (DTRACK (I)), I = 1, MTRACK ),
c$$$     &                 SNGL (CTRACK)
*  +-------------------------------------------------------------------*
*  |  Quenching is activated
      IF ( LQEMGD ) THEN
         IF ( MTRACK .GT. 0 ) THEN
            RULLL  = ZERZER
            CALL QUENMG ( ICODE, MREG, RULLL, DTQUEN )
c$$$            WRITE (IODRAW) ( ( SNGL (DTQUEN (I,JBK)), I = 1, MTRACK ),
c$$$     &                         JBK = 1, NQEMGD )
D           IF ( ICHRGE (JTRACK) .EQ. 0 )
D    &         CALL FLABRT ( 'MGDRAW', 'MTRACK>0 && ICH == 0' )
D           IF ( MEDFLK (MREG,IPRODC) .LE. 2 )
D    &         CALL FLABRT ( 'MGDRAW', 'MTRACK>0 && MEDIUM <= 2' )
D        ELSE
D           IF ( MEDFLK (MREG,IPRODC) .GT. 2
D    &          .AND. ICHRGE (JTRACK) .NE. 0 )
D    &      CALL FLABRT ( 'MGDRAW', 'MTRACK=0 .NEQV. MEDIUM <=2' )
         END IF
      END IF
*  |  End of quenching
*  +-------------------------------------------------------------------*
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
      
      IF(MREG.EQ.IREGSTART.AND.NEWREG.EQ.IREGEND) THEN
*     write particles crossing interface plane on file. 
*     check if heavy ion and calculate mass differently in that case
         IF ( JTRACK .GE. -6 ) THEN ! If the present particle is not a heavy ion with unmber < -6
            AA = AM     (JTRACK) ! Mass
*            IZ = ICHRGE (JTRACK) ! Charge
*            IA = IBARCH (JTRACK) ! Mass number ?
         ELSE
            AA = AMNHEA (-JTRACK) ! Mass
*            IZ = ICHEAV (-JTRACK) ! Charge
*            IA = IBHEAV (-JTRACK) ! Mass number
         ENDIF 

*     ATRACK is the time passed since the primary started. See http://www.fluka.org/web_archive/earchive/new-fluka-discuss/2361.html
         write(66,'(I6,1x,I6,1x,I6,14(1x,e13.6))') 
     &        nint(runNr),ncase,JTRACK, ! ID of primary, particle type
     &        etrack-AA,wtrack, ! kinetic energy of particle (tot. en. - mass), statistical weight of particle
     &        XSCO,YSCO,CXTRCK,CYTRCK,ATRACK, ! x,y, directional cosines at interface plane,time since start of primary
     &        etrack,xStart,yStart,zStart,tStart,
*     &        ,xtrack(0),ytrack(0),ztrack(0) ! total energy, coordinates of initial proton
     &        SPAUSR(1), SPAUSR(2), SPAUSR(3) ! only non-zero if it's a muon. x,y,z coordinates of origin of creation.
      ENDIF


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

