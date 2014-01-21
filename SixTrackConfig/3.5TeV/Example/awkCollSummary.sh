#!/usr/bin/awk -f

# program to create a coll_summary.dat file from a impacts_real or FLUKA_impacts file
# that way we can have a coll_summary which is corrected -- that is, contains only the real impacts, as opposed to the standard coll_summary.dat
# output file awkCollSum.dat is of the format 
# {collimator_ID   n.o. absorbed particles}

# program has been benchmarked with the FLUKA_impacts file and then reproduces the counts in coll_summary.dat
# however, watch out: if some of the particles with multiple entries in FLUKA_impacts file would be cleaned by CleanInelastic, only the last entry is cleaned! The particle thus remains in the impacts_real file and will be counted instead on its first hit. The size of this error should however be negligible - in tries, about 3 particles out of 4783 at primary collimator.

# example call
# ./awkCollSummary.sh impacts_real.dat

BEGIN {
# Code executed once in the beginning
# ####################################

# array containing the count at each collimator
    for (i=1; i <= 500; i++) {
	collcount[i]=0;
	}

# array containing the collimator at which a certain particle ID has hit before
# (some particles appear several times in the impact files but only the last entry should be counted)
    for (i=1; i<=7000; i++) {
	partHitList[i]=0;
    }
    
}

{
# Code executed once for each line in file
# ####################################

# check if particle has already hit another collimator
    if (partHitList[$9] > 0) {
	collcount[partHitList[$9]] = collcount[partHitList[$9]]-1    #decrease count by 1 for collimator that was hit before (only last hit in file counts)
    } 

# increase count at hit collimator
    collcount[$1]=collcount[$1]+1

# set flag that this particle has been counted at this particular collimator
    partHitList[$9]=$1
}

END {
# Code executed once in the end
# ####################################
# end, now output the total

# print out radial binnings to output file
    for (i=1; i <= 500; i++) {
	print i,collcount[i] >> "awkCollSum.dat";
    	}
}
