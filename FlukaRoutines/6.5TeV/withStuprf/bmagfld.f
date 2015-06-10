*      PROGRAM TEST
*      INCLUDE '(DBLPRC)'
*      INCLUDE '(DIMPAR)'
*      INCLUDE '(IOUNIT)'
*
*      CHARACTER*16 FILENAME
*
*      CALL MAGCNST(1, 1.0D0, 0D0, 0D0, 1D0)
*
*      FILENAME="QUAD.dat"
*      CALL MAGLOAD(2,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      FILENAME="MB.dat"
*      CALL MAGLOAD(3,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      FILENAME="MCBC.dat"
*      CALL MAGLOAD(4,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      FILENAME="MQTL.dat"
*      CALL MAGLOAD(5,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      FILENAME="MQW.dat"
*      CALL MAGLOAD(6,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      FILENAME="MB.dat"
*      CALL MAGLOAD(7,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      FILENAME="MBXW.dat"
*      CALL MAGLOAD(7,FILENAME,1.0D0,0D0,0D0,0D0,0D0,0D0,0D0)
*
*      CALL MAGPRINT
*
*      DO Y=-40.0,40.0,1.0
*         DO X=-40.0,40.0,1.0
*            CALL MAGFLD(X,Y,0.0D0,BTX,BTY,BTZ,B,7,IDISC)
**            CALL MAGFLD2(X,Y,0.0D0,BTX,BTY,BTZ,B,6,IDISC)
*            PRINT *,X,Y,BTX*B,BTY*B
*         END DO
*      END DO
*      RETURN
*      END

*$ CREATE MAGFLD.FOR
*COPY MAGFLD
*
*===magfld=============================================================*
*
      SUBROUTINE MAGFLD ( X, Y, Z, BTX, BTY, BTZ, B, NREG, IDISC )

*
*----------------------------------------------------------------------*
*                                                                      *
*     Created  in 2004    by     Vasilis.Vlachoudis@cern.ch            *
*                                                                      *
*     Input variables:                                                 *
*            x,y,z = current position                                  *
*            nreg  = current region                                    *
*     Output variables:                                                *
*            btx,bty,btz = cosines of the magn. field vector           *
*            B = magnetic field intensity (Tesla)                      *
*            idisc = set to 1 if the particle has to be discarded      *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE 'bmagfld.ftn'
*
      include '(GLTLOC)'
      include '(LTCLCM)'
      include '(TRACKR)'

****************************************************
***** Handle the Special type of the MB field ******
****************************************************
      PARAMETER (DMB=1430.0D0)          ! Length
      PARAMETER (FMB=0.005099988074D0)  ! Angle
      PARAMETER (RMB=DMB/FMB)           ! Radius
****************************************************
***** Handle crab cavity field                ******
****************************************************
      PARAMETER (RINGLEN=26658.8832D2)  ! LHC length [cm]
      PARAMETER (HRF400=35640D0)        ! LHC harmonic number
      PARAMETER (OMEGA=TWOPIP*HRF400/RINGLEN*CLIGHT) ! Cavity angular frequency
****************************************************

      LOGICAL LX, LY, LZ
*      INTEGER IERRCNT
*      DATA IERRCNT / 0 /
*      SAVE IERRCNT
*
      LOGICAL LFIRST
      SAVE LFIRST
      DATA LFIRST / .TRUE. /
      IF ( LFIRST ) THEN
         LFIRST = .FALSE.
         CALL MAGPRINT
      END IF
*
      IDISC = 0

* Check the field type based either on lattic first and
* then on region
      IF (MLATTC.GT.0) THEN
         NR = MLATTC    ! We are in a lattic
      ELSE
         NR = NREG      ! Use the region number
      ENDIF
* Lattice based

      NF = NFREG(NR)
      IF (NF.EQ.0) THEN
          BTX = ZERZER
          BTY = ONEONE
          BTZ = ZERZER
          B   = ZERZER
*         WRITE (LUNERR,*)
*     &      ' magfld.f called in zone ',NR,' where there should'
*         WRITE (LUNERR,*)
*     &      ' be no magnetic field. Something is wrong'
*         WRITE (LUNERR,*) ' REGION=',NREG,' LATTICE=',MLATTC
*         IDISC = 1
*         IERRCNT = IERRCNT+1
*         IF (IERRCNT.GT.100)
*     +        CALL FLABRT('MAGFLD',
*     +                    'Too many errors in the magnetic field.')
         RETURN
      ENDIF

      ITYPE = IFTYP(NF)

      IF (ITYPE.NE.NFTCONST.AND.ITYPE.NE.NFTKICKSIN) THEN
          ISYMM = IFSYM(NF)

* Transform the coordinate system
          TX = X - FOFSX(NR)
          TY = Y - FOFSY(NR)
          TZ = Z - FOFSZ(NR)

          BX = FCXX(NR)*TX + FCXY(NR)*TY + FCXZ(NR)*TZ
          BY = FCYX(NR)*TX + FCYY(NR)*TY + FCYZ(NR)*TZ
          BZ = FCZX(NR)*TX + FCZY(NR)*TY + FCZZ(NR)*TZ

****************************************************
***** Handle the Special type of the MB field ******
****************************************************
          IF (ITYPE.EQ.NFTSPECIAL) THEN
              XSHIFT = RMB - SQRT((RMB+BZ)*(RMB-BZ))
*              PRINT *,'MF-SPECIAL RMB,BX,BY,BZ,XSHIFT*1000.0',
*     +                 RMB,BX,BY,BZ,XSHIFT*1000.0
* The shift of 9mm comes from the positioning of the MB and the geometrical
* description of the bended coils!!!
              BX = BX + XSHIFT -0.9116219D0
          ENDIF

* Check for mirroring on the various axes
          IF (BX.LT.ZERZER .AND. IAND(ISYMM,NFSX).NE.0) THEN
              BX = -BX
              LX = .TRUE.
          ELSE
              LX = .FALSE.
          ENDIF

          IF (BY.LT.ZERZER .AND. IAND(ISYMM,NFSY).NE.0) THEN
              BY = -BY
              LY = .TRUE.
          ELSE
              LY = .FALSE.
          ENDIF

          IF (BZ.LT.ZERZER .AND. IAND(ISZMM,NFSZ).NE.0) THEN
              BZ = -BZ
              LZ = .TRUE.
          ELSE
              LZ = .FALSE.
          ENDIF

****************************************************

* Analytic quadrupole coordinates
          IF (ITYPE.EQ.NFTQUAD .OR. ITYPE.EQ.NFTQUADINT) THEN
             QX = BX - FQORIX(NF)
             QY = BY - FQORIY(NF)
          ENDIF
      ELSE
* Constant Field
         BTX = FBX (NR)
         BTY = FBY (NR)
         BTZ = FBZ (NR)
         B   = FB  (NR)
         IF (ITYPE.EQ.NFTKICKSIN) THEN
            AGE = ATRACK
            DELTAT = AGE-FOFSZ(NR)/CLIGHT
*            WRITE (66,111)
*     +           X, Y, Z, OMEGA, AGE, FOFSZ(NR)/CLIGHT, DELTAT,
*     +           SIN( OMEGA * DELTAT )
* 111        FORMAT(8(1X,E15.9))
            B = B * SIN( OMEGA * DELTAT )
            IF( B.LT.ZERZER) THEN
               B = -B
               BTX = -BTX
               BTY = -BTY
               BTZ = -BTZ
            ENDIF
         ENDIF
         RETURN
      ENDIF

* Default
      BTX = ZERZER
      BTY = ONEONE
      BTZ = ZERZER
      B   = ZERZER

* Find the field
      GO TO (100, 200, 300, 400, 400, 500), ITYPE

* Type 1: Constant field (based on region)
 100  RETURN    ! Never comes here but keeps compiler happy

* Type 6: 2D Interpolated dipole field, with the core as analytic
 500  CONTINUE
      IF (BX**2+BY**2 .GT. FQRAD(NF)**2) GOTO 400

      BTX = ZERZER
      BTY = FB(NR)
      BTZ = ZERZER
      B   = DABS ( FB(NR) )

      GO TO 490
      RETURN

* Type 2: 2D Perfect Quadrupole
 200  CONTINUE
         IF (QX**2+QY**2 .GT. FQRAD(NF)**2) RETURN

 210     BTX = QY * FB(NR)
         BTY = QX * FB(NR)
         BTZ = ZERZER
         B   = SQRT(BTX**2 + BTY**2)

         GO TO 490
      RETURN

* Type 3: 2D Interpolated Quadrupole, with the core as analytic
 300  CONTINUE
         IF (QX**2+QY**2 .LE. FQRAD(NF)**2) GO TO 210    ! Use the perfect field
         ! ELSE perform a 2D interpolation
         ! followed below at 400

* Type 4: 2D Interpolation
 400  CONTINUE
         RIX = (BX - FMINX(NF)) / FSTEX(NF)
         iX  = INT(RIX)
         IF (RIX.LT.ZERZER .OR. iX.GE.NBINX(NF)-1) RETURN
         DX  = RIX - DBLE(iX)

         RIY = (BY - FMINY(NF)) / FSTEY(NF)
         iY  = INT(RIY)
         IF (RIY.LT.ZERZER .OR. iY.GE.NBINY(NF)-1) RETURN
         DY  = RIY - DBLE(iY)

         ! Find grid pointers
         iXP    = IPTRBX(NF)
         iYP    = IPTRBY(NF)

         iXY   = iY*NBINX(NF) + iX      ! (x,y)
         iX1Y  = iXY+1                  ! (x+1,y)
         iXY1  = iXY+NBINX(NF)          ! (x,y+1)
         iX1Y1 = iXY1+1                 ! (x+1,y+1)

         ! Perform a 4 point interpolation
         B1 = SIGGTT(iXP+iXY) +DX*(SIGGTT(iXP+iX1Y) -SIGGTT(iXP+iXY))
         B2 = SIGGTT(iXP+iXY1)+DX*(SIGGTT(iXP+iX1Y1)-SIGGTT(iXP+iXY1))
         BX = B1 + DY*(B2-B1)


         B1 = SIGGTT(iYP+iXY) +DX*(SIGGTT(iYP+iX1Y) -SIGGTT(iYP+iXY))
         B2 = SIGGTT(iYP+iXY1)+DX*(SIGGTT(iYP+iX1Y1)-SIGGTT(iYP+iXY1))
         BY = B1 + DY*(B2-B1)

         BTX = BX * FB(NR)
         BTY = BY * FB(NR)
         B   = SQRT(BTX**2 + BTY**2)

  490    IF (B .LT. 1.0D-8) THEN
             BTX = ZERZER
             BTY = ONEONE
             BTZ = ZERZER
             B   = ZERZER
             RETURN
         ENDIF

         BTX = BTX / B
         BTY = BTY / B

         IF (LX) BTY = -BTY
         IF (LY) BTX = -BTX

* Do the inverse transformation
         TX = BTX
         TY = BTY
         TZ = BTZ
         BTX = FCXX(NR)*TX + FCYX(NR)*TY + FCZX(NR)*TZ
         BTY = FCXY(NR)*TX + FCYY(NR)*TY + FCZY(NR)*TZ
         BTZ = FCXZ(NR)*TX + FCYZ(NR)*TY + FCZZ(NR)*TZ
      RETURN
*=== End of subroutine magfld =========================================*
      END

*===magusrini==========================================================*
*
      SUBROUTINE MAGUSRINI( WHAT, SDUM )
* USRINI for handling magnetic fields

      INCLUDE 'bmagfld.ftn'
      INCLUDE '(CMEMFL)'
*
      DIMENSION WHAT (6)
      CHARACTER SDUM*8

      CHARACTER*16 FILENAME

      SAVE  NREGFROM, NREGTO, NSTEP
      SAVE  FIELD, FILENAME

* Skip leading blanks of SDUM
*      I = 1
*      DO WHILE (I.LT.8 .AND. SDUM(I:I).EQ.' ')
*         I= I+1
*      ENDDO
*      IF (I.GT.1) SDUM=SDUM(I:8)

* Common Cards
      IF (SDUM.NE.'&') THEN
          NREGFROM = NINT(WHAT(2))
          NREGTO   = NINT(WHAT(3))
          NSTEP    = NINT(WHAT(4))
          FIELD    = WHAT(5)

          IF (NREGFROM.LT.1 .OR. NREGFROM.GT.MXXRGN)
     +        CALL FLABRT('MAGUSRINI',
     +                    'Invalid Region number in WHAT(2)')
          IF (NREGTO.EQ.0) NREGTO = NREGFROM
          IF (NSTEP.LE.0)  NSTEP  = 1

          FILENAME = SDUM
      ELSE
* Constant Field
         IF ( FILENAME.EQ.'CONST'.OR.
     +        FILENAME.EQ.'KICKSIN') THEN
            NFTYPE = 0
            IF (FILENAME.EQ.'CONST') THEN
               NFTYPE = NFTCONST
            ELSE IF (FILENAME.EQ.'KICKSIN') THEN
               NFTYPE = NFTKICKSIN
            ELSE
               CALL FLABRT('MAGCNST',
     +              'Field type not allowed '//FILENAME)
            ENDIF

            DO I=NREGFROM,NREGTO,NSTEP
               CALL MAGCNST(I,FIELD,WHAT(1),WHAT(2),WHAT(3),WHAT(6),
     +              NFTYPE)
            ENDDO
         ELSE
             FILENAME=FILENAME(1:INDEX(FILENAME,' ')-1)//'.dat'
             DO I=NREGFROM,NREGTO,NSTEP
                 CALL MAGLOAD(I, FILENAME, FIELD,
     +                        WHAT(1),WHAT(2),WHAT(3),
     +                        WHAT(4),WHAT(5),WHAT(6))
             ENDDO
         ENDIF
      ENDIF

*=== End of subroutine magusrini=======================================*
      END

*===magcnst============================================================*
*
      SUBROUTINE MAGCNST( NREG, B, BX, BY, BZ, ZOFS, NFTYPE )
* Create a new constant field

      INCLUDE 'bmagfld.ftn'
*
      CHARACTER*16 FNAME
      CHARACTER*1 STRING
      WRITE (STRING, '(I1)') NFTYPE
      FNAME = 'Internal'//STRING
* Search if it is already loaded and simply assign it to the region
      DO NF=1,NFIELD
         IF (FFILE(NF).EQ.FNAME) THEN
            NFREG (NREG) = NF
            GOTO 10
         ENDIF
      ENDDO

* New field
      NFIELD = NFIELD + 1
      IF (NFIELD.GT.MXFLDS)
     +    CALL FLABRT('MAGCNST','Increase MXFLDS')

* Default Values
      NFREG (NREG)   = NFIELD
      FFILE (NFIELD) = FNAME
      IFTYP (NFIELD) = NFTYPE
      IFSYM (NFIELD) = NFSNONE

10    CONTINUE
      BLEN = SQRT(BX**2+BY**2+BZ**2)
      FBX   (NREG) = BX/BLEN
      FBY   (NREG) = BY/BLEN
      FBZ   (NREG) = BZ/BLEN
      FOFSZ (NREG) = ZOFS
      FB    (NREG) = B

      IF (FB(NREG).LT.ZERZER) THEN
         FB  (NREG) = -FB  (NREG)
         FBX (NREG) = -FBX (NREG)
         FBY (NREG) = -FBY (NREG)
         FBZ (NREG) = -FBZ (NREG)
      ENDIF
      RETURN
*=== End of subroutine magcnst=========================================*
      END

*
*===magload============================================================*
*
      SUBROUTINE MAGLOAD( NREG, FILENAME, FIELD,
     +                    XOFS, YOFS, ZOFS,
     +                    RX,   RY,   RZ )

      INCLUDE 'bmagfld.ftn'
      DATA  NFIELD / 0 /

* Arguments
      CHARACTER*16 FILENAME

* Local variables
      CHARACTER*250 LINE
      CHARACTER*16  CARD
      LOGICAL       LERR, LFOUND

      PARAMETER (MXFTYP = 7)
      CHARACTER*8  FTYPE(MXFTYP)
      DATA FTYPE / 'CONST', 'QUAD', 'QUADINT', 'INTER2D', 'SPECIAL',
     &     'KICKINT', 'KICKSIN' /

      LERR = .FALSE.

* Search if it is already loaded and simply assign it to the region
      LFOUND = .FALSE.
      DO NF=1,NFIELD
         IF (FFILE(NF).EQ.FILENAME) THEN
            LFOUND = .TRUE.
            GOTO 10
         ENDIF
      ENDDO

* Load a new file
      NFIELD = NFIELD + 1
      IF (NFIELD.GT.MXFLDS)
     +    CALL FLABRT('LOADMAGF','Increase MXFLDS')
      NF = NFIELD

* Default Values
10    CONTINUE

      NFREG (NREG) = NF

* Transformation
      FOFSX (NREG) = XOFS
      FOFSY (NREG) = YOFS
      FOFSZ (NREG) = ZOFS

      CX = COS(RX)
      SX = SIN(RX)
      CY = COS(RY)
      SY = SIN(RY)
      CZ = COS(RZ)
      SZ = SIN(RZ)

* Rotation order X->Y->Z
      FCXX (NREG) =  CY*CZ
      FCXY (NREG) =  CX*SZ+CZ*SX*SY
      FCXZ (NREG) =  SX*SZ-CX*CZ*SY

      FCYX (NREG) = -CY*SZ
      FCYY (NREG) =  CX*CZ-SX*SY*SZ
      FCYZ (NREG) =  CX*SY*SZ+CZ*SX

      FCZX (NREG) =  SY
      FCZY (NREG) = -CY*SX
      FCZZ (NREG) =  CX*CY

      FB   (NREG)  = FIELD
      FBX  (NREG)  = ZERZER
      FBY  (NREG)  = ZERZER
      FBZ  (NREG)  = ONEONE

      IF (LFOUND) RETURN

* Field
      FFILE (NF)  = FILENAME

      NBINX (NF)  = 0
      NBINY (NF)  = 0
      IFTYP (NF)  = 0
      IFSYM (NF)  = 0
      IPTRBX(NF)  = 0
      IPTRBY(NF)  = 0

      CALL OAUXFI(FILENAME,LUNRDB,'OLD',IERR)
      IF ( IERR .GT. 0 )
     +    CALL FLABRT('LOADMAGF','Error opening file '//FILENAME)

* Parse the file
100   CONTINUE
         READ (LUNRDB, '(A)', ERR=999, END=200 ) LINE
*         WRITE(LUNERR,*) 'LINE=',LINE
         ! Strip comments
         IF (LINE(1:1).EQ.'#') GO TO 100
         I = INDEX(LINE,'#')
         IF (I.GT.0) LINE = LINE(1:I-1)
         IF (LINE.EQ.' ') GO TO 100

* Find card and arguments
         ISPACE = INDEX(LINE,' ')
         CARD = LINE(1:ISPACE-1)
         DO WHILE (ISPACE.LT.250 .AND. LINE(ISPACE:ISPACE).EQ.' ')
            ISPACE = ISPACE+1
         ENDDO
         LINE = LINE(ISPACE:250)

*         WRITE(LUNERR,*) '   CARD=',CARD
*         WRITE(LUNERR,*) '   ARGS=',LINE

* --- Check the field type ---
         IF (CARD .EQ. 'TYPE') THEN
              IFTYP(NF) = 0
              DO I=1,MXFTYP
                 IF (FTYPE(I).EQ.LINE) THEN
                    IFTYP(NF) = I
                 ENDIF
              ENDDO
              IF (IFTYP(NF).EQ.0)
     +           CALL FLABRT('LOADMAGF','Invalid field type '//LINE)

* --- Check the field symmetry ---
         ELSE IF (CARD .EQ. 'SYMMETRY') THEN
              IFSYM(NF) = NFS0
              DO I=1,250
                 IF (LINE(I:I).EQ.'X') THEN
                    IFSYM(NF) = IOR(IFSYM(NF),NFSX)
                 ELSE IF (LINE(I:I).EQ.'Y') THEN
                    IFSYM(NF) = IOR(IFSYM(NF),NFSY)
                 ELSE IF (LINE(I:I).EQ.'Z') THEN
                    IFSYM(NF) = IOR(IFSYM(NF),NFSZ)
                 ENDIF
              ENDDO

* --- Read Quadrupole Origin position ---
         ELSE IF (CARD .EQ. 'QORIGIN') THEN
              READ(LINE,*) FQORIX(NF),
     +                     FQORIY(NF),
     +                     FQORIZ(NF)

* --- Read Quadrupole field Radius ---
         ELSE IF (CARD .EQ. 'QRADIUS') THEN
              READ(LINE,*) FQRAD(NF)

* --- Read the grid information min, max and bins ---
         ELSE IF (CARD .EQ. 'XGRID') THEN
              READ(LINE,*) FMINX(NF),
     +                     FMAXX(NF),
     +                     NBINX(NF)

              FSTEX(NF) = (FMAXX(NF)-FMINX(NF))
     +                         / DBLE(NBINX(NF)-1)

* --- Read the grid information min, max and bins ---
         ELSE IF (CARD .EQ. 'YGRID') THEN
              READ(LINE,*) FMINY(NF),
     +                     FMAXY(NF),
     +                     NBINY(NF)

              FSTEY(NF) = (FMAXY(NF)-FMINY(NF))
     +                         / DBLE(NBINY(NF)-1)

* --- Read the interpolation data for the B components ---
         ELSE IF (CARD .EQ. 'DATA') THEN
             ! WARNING the values are defined on the verteces
             ! of the grid so we have NBIN[XY] + 1 values to read

             ! Get the last used memory position
*             IF (IFTYP(NF).LE.NFTINT2D) THEN
                 ! 2D - interpolations...

                 ! --- Allocate memory in SIGGTT ---
                 N = NBINX(NF) * NBINY(NF)

                 IPTRBX(NF) = KBLNKL+1
                 IPTRBY(NF) = KBLNKL+1+N

                 ! Update the last used memory position
                 KBLNKL = KBLNKL + 2*N
                 IF (KBLNKL.GE.MBLNMX)
     +               CALL FLABRT('MAGLOAD',
     +                     'Not enough memory. Increase MBLNMX')

                 ! Read the data
                 DO I=0,N-1
                    READ(LUNRDB,*) SIGGTT(IPTRBX(NF)+I),
     +                             SIGGTT(IPTRBY(NF)+I)
                 END DO
*             ENDIF
         ELSE
              WRITE(LUNERR,*) 'Unknown card in file ',FILENAME,
     +                        ' CARD=',CARD,' LINE=',LINE
              LERR = .TRUE.
         ENDIF
      GOTO 100

* End of File
200   CONTINUE

      IF (LERR) GOTO 999

      CLOSE (UNIT=LUNRDB)
      RETURN

910   FORMAT(3X,2I4,6(F8.4,1X))

* Error
999   CALL FLABRT('LOADMAGF','Error while reading file '//FILENAME)
*=== End of subroutine magload ========================================*
      END

*===magprint===========================================================*
*
      SUBROUTINE MAGPRINT( )

      INCLUDE 'bmagfld.ftn'

      PARAMETER (MXFTYP = 7)
      CHARACTER*8  FTYPE(MXFTYP)
      DATA FTYPE / 'CONST', 'QUAD', 'QUADINT', 'INTER2D', 'SPECIAL',
     &     'KICKINT', 'KICKSIN' /

      PARAMETER (MXFSYM = 8)
      CHARACTER*4  FSYMM(MXFSYM)
*                  000  001  010   011  100   101   110   111
      DATA FSYMM / '-', 'X', 'Y', 'XY', 'Z', 'XZ', 'YZ', 'XYZ' /

* Print Fields
      WRITE (LUNOUT,*)
      WRITE (LUNOUT,*) '*** Magnetic Fields ***'
      WRITE (LUNOUT,*) 'TOTAL FIELDS LOADED: ',NFIELD
      DO 10 NF=1,NFIELD
         WRITE(LUNOUT,*) 'FIELD #  ',NF
         WRITE(LUNOUT,*) '   FILENAME ',FFILE(NF)
         WRITE(LUNOUT,*) '   TYPE     ',FTYPE(IFTYP(NF)),
     +                              ' ',IFTYP(NF)
         IF (IFTYP(NF).EQ.NFTCONST.OR.IFTYP(NF).EQ.NFTKICKSIN) GOTO 10

         WRITE(LUNOUT,*) '   SYMMETRY ',FSYMM(IFSYM(NF)+1),
     +                                  IFSYM(NF)
         WRITE(LUNOUT,*) '   QORIGIN  ',FQORIX(NF), FQORIY(NF),
     +                                  FQORIZ(NF)
         WRITE(LUNOUT,*) '   QRADIUS  ',FQRAD (NF)
         IF (IFTYP(NF).EQ.NFTQUAD) GOTO 10

         WRITE(LUNOUT,*) '   XGRID    ',FMINX(NF), FMAXX(NF),
     +                                  NBINX(NF), FSTEX(NF)
         WRITE(LUNOUT,*) '   YGRID    ',FMINY(NF), FMAXY(NF),
     +                                  NBINY(NF), FSTEY(NF)
*         DO J=0,NBINY(NF)-1
*            DO I=0,NBINX(NF)-1
*                WRITE(LUNOUT,810) I,J,
*     +                FMINX(NF)+I*FSTEX(NF),
*     +                FMINY(NF)+J*FSTEY(NF),
*     +                SIGGTT(IPTRBX(NF)+J*NBINX(NF)+I),
*     +                SIGGTT(IPTRBY(NF)+J*NBINX(NF)+I)
*            ENDDO
*         ENDDO
 10   CONTINUE

810   FORMAT(3X,2I4,6(F8.4,1X))

      WRITE (LUNOUT,*)
      WRITE (LUNOUT,*) '*** Magnetic Field: Region Assignments ***'
      DO NR=1,MXXRGN
         NF = NFREG(NR)
         IF (NF.NE.0) THEN
            WRITE (LUNOUT,900) NR,NF,FFILE(NF),FTYPE(IFTYP(NF))
            WRITE (LUNOUT,901) FB(NR)
            IF (IFTYP(NF).EQ.NFTCONST.OR.IFTYP(NF).EQ.NFTKICKSIN)
     +          WRITE (LUNOUT,902) FBX(NR),FBY(NR),FBZ(NR)
            WRITE (LUNOUT,903) FOFSX(NR), FOFSY(NR), FOFSZ(NR)
            WRITE (LUNOUT,*)   '   Transformation Matrix'
            WRITE (LUNOUT,904) FCXX(NR), FCXY(NR), FCXZ(NR)
            WRITE (LUNOUT,904) FCYX(NR), FCYY(NR), FCYZ(NR)
            WRITE (LUNOUT,904) FCZX(NR), FCZY(NR), FCZZ(NR)
            WRITE (LUNOUT,*)
         ENDIF
      ENDDO

900   FORMAT('Reg=',I5,' FieldId=',I3,'  File=',A16,' Type=',A8,1X,I3)
901   FORMAT(3X,'Field= ',F15.6)
902   FORMAT(3X,'Dir=   ',3(F15.6,1X))
903   FORMAT(3X,'Offset=',3(F15.6,1X))
904   FORMAT(6X,3(F10.5,1X))

      RETURN
*=== End of subroutine magprint========================================*
      END
