#
#
#
#
#
#
#
export FLUKA=/afs/cern.ch/work/r/rkwee/Fluka/fluka20112blinuxAA
export FLUPRO=/afs/cern.ch/work/r/rkwee/Fluka/fluka20112blinuxAA/

FFF=$(FLUKA)/flutil/fff
LFLUKA=$(FLUKA)/flutil/lfluka
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
	$(LFLUKA) -m fluka -o ir1_4TeV.exe $^
#
#
clean:
	rm -f *.exe *.o *.map *.FOR
#
