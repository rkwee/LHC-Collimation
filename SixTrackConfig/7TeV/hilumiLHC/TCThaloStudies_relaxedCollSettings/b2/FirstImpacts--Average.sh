#!/bin/bash
awk '$1>0 {sum+=$7} END { print "Average x_in = ",sum/(NR-1)}' FirstImpacts.dat
awk '$1>0 {sum+=$11} END { print "Average x_out = ",sum/(NR-1)}' FirstImpacts.dat
