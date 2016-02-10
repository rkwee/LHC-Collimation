*$ CREATE USRINI.FOR
*COPY USRINI
*
*=== usrini ===========================================================*
*
      SUBROUTINE USRINI ( WHAT, SDUM )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 1991-2005      by    Alfredo Ferrari & Paola Sala  *
*     All Rights Reserved.                                             *
*                                                                      *
*                                                                      *
*     USeR INItialization: this routine is called every time the       *
*                          USRICALL card is found in the input stream  *
*                                                                      *
*                                                                      *
*     Created on 01 january 1991   by    Alfredo Ferrari & Paola Sala  *
*                                                   Infn - Milan       *
*                                                                      *
*     Last change on 24-Jul-13     by    Francesco Cerutti             *
*                                                                      *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE 'COLSPE.inc'
*
      DIMENSION WHAT (6)
      CHARACTER SDUM*8
*
      LOGICAL LFIRST
*
      DATA LFIRST /.TRUE./
*
*  association to each collimator of (its length and) the ROT-DEFI
*  transform. bringing its center from the origin to the actual position
*  [USRICALLs are automatically generated as the geometry
*  is created by the LineBuilder] 
*
      IF (LFIRST) THEN
         DO ICOLIN=1,NCOLLI
*  ROT-DEFI index
            ITRACL(ICOLIN) = -1 
*  collimator length
            COLLEN(ICOLIN) = -999.999D0
         ENDDO
         LFIRST = .FALSE.
      END IF
*
*  Don't change the following line:
      LUSRIN = .TRUE.
* *** Write from here on *** *
      ICOLIN = NINT(WHAT(1))
      IF (ICOLIN.LT.1) THEN
         CALL FLABRT('USRINI','ICOLIN < 1 ?!')
      ELSE IF (ICOLIN.GT.NCOLLI) THEN
         CALL FLABRT('USRINI','Increase NCOLLI in COLSPE.inc')
      END IF
      COLLEN(ICOLIN) = WHAT(2)
      ITRACL(ICOLIN) = NINT(WHAT(3))
      RETURN
*=== End of subroutine Usrini =========================================*
      END
