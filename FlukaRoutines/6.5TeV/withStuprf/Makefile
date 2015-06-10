#
#
#
#
#
#
#
export FLUKA=/afs/cern.ch/work/r/rkwee/Fluka/fluka20112clinuxAA
export FLUPRO=/afs/cern.ch/work/r/rkwee/Fluka/fluka20112clinuxAA/

EXENAME=run2
FFF=$(FLUKA)/flutil/fff
LFLUKA=$(FLUKA)/flutil/lfluka # accoring to Luigi this works until 20 TeV lab frame (6.48 CME)
#LFLUKA=$(FLUKA)/flutil/ldpm3qmd
#
#
SRCFILES:=$(shell ls *.f | grep -v includ)
OBJECTS:=$(patsubst %.f, %.o, $(SRCFILES))
#
#
############# RULES ###############
#
#
.f.o:
	$(FFF) $<
#
############# TARGETS #############
#
all: exe_tct_impacts
#
#
exe_tct_impacts: $(OBJECTS)
	echo $(OBJECTS) 
	$(LFLUKA) -m fluka -o $(EXENAME).exe $^
#
#
clean:
	rm -f *.exe *.o *.map *.FOR
#
