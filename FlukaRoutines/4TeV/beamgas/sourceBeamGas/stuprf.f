*$ CREATE STUPRF.FOR
*COPY STUPRF
*
*=== stuprf ===========================================================*
*
      SUBROUTINE STUPRF ( IJ, MREG, XX, YY, ZZ, NPSECN, NPPRMR )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
* -- rkwee
      INCLUDE '(GENSTK)'
      INCLUDE '(PAPROP)' 
* -- 
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1997-2005      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*                                                                      *
*     SeT User PRoperties for Fluka particles:                         *
*                                                                      *
*     Created on  09 october 1997  by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*     Last change on  14-jul-05    by    Alfredo Ferrari               *
*                                                                      *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE '(EVTFLG)'
      INCLUDE '(FLKSTK)'
      INCLUDE '(TRACKR)'
*
      LOUSE   (NPFLKA)  = LLOUSE
      DO 100 ISPR = 1, MKBMX1
         SPAREK (ISPR,NPFLKA) = SPAUSR (ISPR)
  100 CONTINUE
      DO 200 ISPR = 1, MKBMX2
         ISPARK (ISPR,NPFLKA) = ISPUSR (ISPR)
  200 CONTINUE
* -- rkwee dump muon origin
      IF ( ( IJ .NE. 10 .AND. KPART (NPSECN) .EQ. 10 ) .OR.
     &     ( IJ .NE. 11 .AND. KPART (NPSECN) .EQ. 11 ) ) THEN
*       Coordinates where muon was created:
          SPAREK( 5, NPFLKA ) = XX
          SPAREK( 6, NPFLKA ) = YY
          SPAREK( 7, NPFLKA ) = ZZ

*          WRITE(*,*) "rkwee:", XX, YY, ZZ
*        Kinetic energy of the created muon:
          SPAREK( 8, NPFLKA ) = TKI( NPSECN )
*        Kinetic energy of parent:
          SPAREK( 9, NPFLKA ) = ETRACK-AM(IJ)
*        Particle ID of parent
          ISPARK( 1, NPFLKA ) = IJ
       END IF
* -- 
*  Increment the track number and put it into the last flag:
      IF ( NPSECN .GT. NPPRMR ) THEN
         IF ( NTRCKS .EQ. 2000000000 ) NTRCKS = -2000000000
         NTRCKS = NTRCKS + 1
         ISPARK (MKBMX2,NPFLKA) = NTRCKS
      END IF
      RETURN
*=== End of subroutine Stuprf =========================================*
      END

