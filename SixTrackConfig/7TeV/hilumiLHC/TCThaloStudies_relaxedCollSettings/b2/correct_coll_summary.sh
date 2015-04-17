#!/bin/bash


if [ $(echo "`wc -l impacts_fake.dat |cut -f 1 -d ' '` > 1" |bc -l) = 1 ];then
	cp coll_summary.dat Coll_Summary.original.dat
	awk 'NR>1 {print $1}'  impacts_fake.dat>list
	for i in `cat list`;do
		awk '{if ($1=='$i') {print " ",$1,$2,"\t",$3,"\t",$4-1,"\t",$5,"\t",$6,"\t",$7,"\t"}else{print " ",$1,$2,"\t",$3,"\t",$4,"\t",$5,"\t",$6,"\t",$7,"\t"} }' coll_summary.dat > temp
	       cp temp	coll_summary.dat
       done
fi
     
       
