#!/usr/bin/python
#
#
# rkwee, Sept 2015
# ------------------------------------------------------------------------------------------------
import os, math, time, ROOT, sys
from ROOT import *

# dictionary of timber variables
vDictTCTs = {  
    "BLMTI.04L1.B1I10_TCTPH.4L1.B1:LOSS_RS09" : [kBlue,  33, ],
    "BLMTI.04L1.B1I10_TCTPV.4L1.B1:LOSS_RS09" : [kBlue-2,34, ],
    "BLMTI.04L5.B1I10_TCTPH.4L5.B1:LOSS_RS09" : [kRed+1, 22, ],
    "BLMTI.04L5.B1I10_TCTPV.4L5.B1:LOSS_RS09" : [kRed-2, 23, ],

    "BLMTI.04R1.B2I10_TCTPH.4R1.B2:LOSS_RS09" : [kCyan+2, 27, ],
    "BLMTI.04R1.B2I10_TCTPV.4R1.B2:LOSS_RS09" : [kGreen-2,28, ],
    "BLMTI.04R5.B2I10_TCTPH.4R5.B2:LOSS_RS09" : [kPink-3, 26, ],
    "BLMTI.04R5.B2I10_TCTPV.4R5.B2:LOSS_RS09" : [kPink+1, 28, ],
}
# ------------------------------------------------------------------------------------------------
# not only primaries....
vDictTCPs = {  

    "BLMEI.06L7.B1E10_TCHSV.6L7.B1:LOSS_RS09" : [kYellow+2, 20], 
    "BLMEI.06L7.B1E10_TCP.A6L7.B1:LOSS_RS09" : [kOrange+6, 24,], 
    "BLMEI.06L7.B1E10_TCSM.A6L7.B1:LOSS_RS09" : [kOrange+4, 28,], 
    "BLMEI.06R7.B2I10_TCHSV.6R7.B2:LOSS_RS09" : [kOrange+3, 26,], 
    "BLMEI.06R7.B2I10_TCP.A6R7.B2:LOSS_RS09" : [kOrange+2, 28,],
    "BLMEI.06R7.B2I10_TCSM.A6R7.B2:LOSS_RS09" : [kOrange+1, 27,],
    "BLMTI.06L7.B2I10_TCLA.A6L7.B2:LOSS_RS09" : [kYellow-2, 33,],
    "BLMTI.06L7.B2I10_TCLA.B6L7.B2:LOSS_RS09" : [kYellow-8,  34,], 
    "BLMTI.06R7.B1E10_TCLA.A6R7.B1:LOSS_RS09" : [kYellow+7,  22,], 
    "BLMTI.06R7.B1E10_TCLA.B6R7.B1:LOSS_RS09" : [kYellow+3,  23,],

}
# ------------------------------------------------------------------------------------------------

timeNoise  = [
        ('2015-08-28 05:50:00','2015-08-28 05:54:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 1
        ('2015-08-28 06:06:00','2015-08-28 06:08:20', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 2
        ('2015-08-28 06:13:01','2015-08-28 06:15:59', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 3
        ('2015-08-28 06:23:00','2015-08-28 06:24:10', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 4
        ('2015-08-28 06:29:01','2015-08-28 06:30:10', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 5
        ('2015-08-28 06:39:01','2015-08-28 06:40:20', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum"),      # 6

        ('2015-08-28 07:28:00','2015-08-28 07:31:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum"),       # 7
        ('2015-08-28 07:38:00','2015-08-28 07:40:00', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 8
        ('2015-08-28 07:45:30','2015-08-28 07:46:20', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 9
        ('2015-08-28 07:50:00','2015-08-28 07:51:30', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum"),      # 10

        ('2015-08-28 08:02:00','2015-08-28 08:05:20', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 11
        ('2015-08-28 08:15:00','2015-08-28 08:17:20', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 12
        ('2015-08-28 08:23:00','2015-08-28 08:25:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 13

        ('2015-08-28 08:31:00','2015-08-28 08:31:20', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 14
        ('2015-08-28 08:39:00','2015-08-28 08:40:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 15
        ('2015-08-28 08:43:00','2015-08-28 08:44:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 16

]
# ------------------------------------------------------------------------------------------------
timeSignal = [

        ('2015-08-28 05:50:00','2015-08-28 06:06:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 1
        ('2015-08-28 06:06:01','2015-08-28 06:13:00', "TCTs at 8.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 2
        ('2015-08-28 06:13:01','2015-08-28 06:23:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 3
        ('2015-08-28 06:23:01','2015-08-28 06:29:00', "TCTs at 9.3#sigma, TCLAs at 14#sigma, on-momentum"),       # 4
        ('2015-08-28 06:29:01','2015-08-28 06:39:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, on-momentum"),       # 5
        ('2015-08-28 06:39:01','2015-08-28 06:53:00', "TCTs at 10.3#sigma, TCLAs at 14#sigma, on-momentum"),      # 6
        ('2015-08-28 07:20:01','2015-08-28 07:38:00', "TCTs at 8.3#sigma, TCLAs at 10#sigma, on-momentum"),       # 7
        ('2015-08-28 07:38:01','2015-08-28 07:45:30', "TCTs at 8.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 8
        ('2015-08-28 07:45:31','2015-08-28 07:50:00', "TCTs at 9.8#sigma, TCLAs at 10#sigma, on-momentum"),       # 9
        ('2015-08-28 07:50:01','2015-08-28 07:55:00', "TCTs at 7.8#sigma, TCLAs at 10#sigma, on-momentum"),      # 10
        ('2015-08-28 07:58:01','2015-08-28 08:14:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 11
        ('2015-08-28 08:14:01','2015-08-28 08:22:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 12
        ('2015-08-28 08:22:01','2015-08-28 08:30:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, neg-off-momentum"), # 13
        ('2015-08-28 08:30:01','2015-08-28 08:36:00', "TCTs at 9.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 14
        ('2015-08-28 08:36:01','2015-08-28 08:43:00', "TCTs at 8.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 15
        ('2015-08-28 08:43:01','2015-08-28 08:48:00', "TCTs at 7.8#sigma, TCLAs at 14#sigma, pos-off-momentum"), # 16
]
# ------------------------------------------------------------------------------------------------
