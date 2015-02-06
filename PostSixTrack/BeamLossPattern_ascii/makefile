
CPP=g++

#CCFLAGS= -Wall -static 

SRC = Aperture.o OneMetre.o ReadTwiss.o AssignOneMetre.o Survey.o OneMetreAlign.o 

default: BeamLossPattern

BeamLossPattern: BeamLossPattern_2005-04-26.o ${SRC}
	${CPP} ${CCFLAGS} -o BeamLossPattern_2005-04-26 BeamLossPattern_2005-04-26.o ${SRC}

GetAperture: GetAperture_2005-06-07.o ${SRC}
	${CPP} ${CCFLAGS} -o GetAperture GetAperture_2005-06-07.o ${SRC}

clean:
	rm -f *.o

%.o: %.cpp
	${CPP} ${CCFLAGS} -c $< -o $@
