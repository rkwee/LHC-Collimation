*$ CREATE USRGLO.FOR
*COPY USRGLO
*
*=== usrglo ===========================================================*
*
      SUBROUTINE USRGLO ( WHAT, SDUM )

      INCLUDE '(DBLPRC)'
      INCLUDE '(DIMPAR)'
      INCLUDE '(IOUNIT)'
*
      DIMENSION WHAT (6)
      CHARACTER SDUM*8
*
      integer ii, NWHAT1
      save nwhat1
      data nwhat1 / -1 /
      
c      LOGICAL LFIRST
c      SAVE LFIRST
c      DATA LFIRST / .TRUE. /
*
*  Don't change the following line:
      LUSRGL = .TRUE.
* *** Write from here on *** *
*
c      IF ( LFIRST ) THEN
c        LFIRST = .FALSE.
c      ENDIF

* Skip leading blanks of SDUM
      ii = 1
      DO WHILE (ii.LT.8 .AND. SDUM(ii:ii).EQ.' ')
         ii= ii+1
      ENDDO
      IF (ii.GT.1) SDUM=SDUM(ii:8)

* Read in the values needed for user magnetic field
* --------------------------------------------------
      IF (SDUM.NE.'&') NWHAT1 = NINT (WHAT(1))
      IF ( NWHAT1.EQ.100 ) THEN
* User defined magnetic field
         CALL MAGUSRINI(WHAT,SDUM)
      ELSE
         CALL MAGPRINT
      ENDIF
*
      RETURN
*=== End of subroutine Usrglb =========================================*
      END
