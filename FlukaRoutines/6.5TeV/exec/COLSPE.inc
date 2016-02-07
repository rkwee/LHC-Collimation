*                                                                      *
*     COLlimator SPEcs                                                 *
*                                                                      *
*     last change   24-Jul-2013         by   Francesco Cerutti         *
*                                                                      *
*            included in :                                             *
*                          source                                      *
*                          usrini                                      *
*                                                                      *
*     common associating to each collimator (its length and)           * 
*     the ROT-DEFI transformation bringing its center from the origin  *
*     to the actual position                                           *
*     [ROT-DEFIs and USRICALLs are automatically generated             *
*     as the geometry is created by the LineBuilder]                   *
*                                                                      *
*----------------------------------------------------------------------*
*                                                                      *
*
      PARAMETER ( NCOLLI = 200 )
      COMMON / COLSPE / COLLEN(NCOLLI), ITRACL(NCOLLI)
*
