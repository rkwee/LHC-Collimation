cmake_minimum_required(VERSION 2.4)

PROJECT(CleanInelastic)

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

if(NOT CMAKE_BUILD_TYPE)
    SET(CMAKE_BUILD_TYPE Debug CACHE STRING
        "Choose the type of build, options are: Debug Release"
        FORCE)
endif(NOT CMAKE_BUILD_TYPE)

option(WITH_OMPI "Set to on when HDF5 is built with OpenMPI" OFF)
option(USE_AFS "Set to on when you need to use libraries on AFS" OFF)

find_package(HDF5)
if(HDF5_FOUND OR USE_AFS)
  option(USE_HDF5 "Set to on if you want to include support for HDF5" ON)
else()
  option(USE_HDF5 "Set to on if you want to include support for HDF5" OFF)
endif()

set(sources Aperture.cpp ReadTracks.cpp OneMetre.cpp ReadTwiss.cpp AssignOneMetre.cpp Survey.cpp OneMetreAlign.cpp)

if (WITH_OMPI) 
    set(CMAKE_CXX_COMPILER "mpic++")
endif (WITH_OMPI) 


add_library(lhccoll ${sources})

if (USE_AFS)
    set(CMAKE_CXX_FLAGS "-m32")
    set(CMAKE_CXX_LINK_FLAGS "-static -m32")
    if(USE_HDF5)
#	set(H5ROOT "/afs/cern.ch/user/y/ylevinse/scratch0/hdf5/hdf5-1.8.6-gcc45/")
#	set(H5ROOT "/afs/cern.ch/work/r/rbruce/BeamLossPattern/hdf5-1.8.6-gcc45/")
	set(H5ROOT "/afs/cern.ch/work/r/rkwee/HL-LHC/SixTrack_slc6_20Oct2014_rev180/withhdf5/hdf5-1.8.14")
        set(HDF5_ROOT "/afs/cern.ch/work/r/rkwee/HL-LHC/SixTrack_slc6_20Oct2014_rev180/withhdf5/hdf5-1.8.14")
        include_directories(${H5ROOT}/include/)
        link_directories(${H5ROOT}/lib/)
        target_link_libraries(lhccoll dl szip hdf5 hdf5_hl hdf5_f90cstub hdf5_fortran hdf5_hl_fortran z m)
    endif(USE_HDF5)
endif (USE_AFS)


add_executable(beamLossPattern BeamLossPattern.cpp)
add_executable(getAperture GetAperture.cpp)
add_executable(cleanInelastic CleanInelastic.cpp)

#add_executable(htest hdtest.cpp)

target_link_libraries(beamLossPattern lhccoll)
target_link_libraries(getAperture lhccoll)

include_directories(${CMAKE_CURRENT_BINARY_DIR})

INCLUDE (CheckIncludeFiles)

if(USE_HDF5 AND NOT USE_AFS)
#     set(HDF5_USE_STATIC_LIBRARIES ON)
    find_package(HDF5 REQUIRED)
    if(HDF5_FOUND)
        include_directories(${HDF5_INCLUDE_DIRS})
        target_link_libraries(beamLossPattern ${HDF5_LIBRARIES})
    #     target_link_libraries(htest ${HDF5_LIBRARIES})
    endif(HDF5_FOUND)
endif(USE_HDF5 AND NOT USE_AFS)

if(USE_HDF5)
    # must come after hdf5 include directories are present
    CHECK_INCLUDE_FILES(hdf5.h HAVE_HDF5_H)
endif(USE_HDF5)

find_package(PythonInterp)

CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/config.h)
ENABLE_TESTING()

add_test(cleanInel_1 ${EXECUTABLE_OUTPUT_PATH}/cleanInelastic
 ${CMAKE_CURRENT_SOURCE_DIR}/test/FLUKA_impacts.dat
 ${CMAKE_CURRENT_SOURCE_DIR}/test/LPI_output.txt.s
 ${CMAKE_CURRENT_SOURCE_DIR}/test/CollPositions.dat
 ${CMAKE_CURRENT_SOURCE_DIR}/test/coll_summary.dat)
add_test(getAper_1 ${EXECUTABLE_OUTPUT_PATH}/getAperture 
 ${CMAKE_CURRENT_SOURCE_DIR}/test/allapert_20080127.b1)
add_test(beamLossPattern_1_small ${EXECUTABLE_OUTPUT_PATH}/beamLossPattern 
 ${CMAKE_CURRENT_SOURCE_DIR}/test/tracks2.dat output-blsm.txt
 ${CMAKE_CURRENT_SOURCE_DIR}/test/allapert_20080127.b1
 ${CMAKE_CURRENT_SOURCE_DIR}/test/SurveyWithCrossing_XP_inj.dat)
if(PYTHONINTERP_FOUND)
add_test(beamLossPattern_2_small ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/comparekLPIs.py ${CMAKE_CURRENT_SOURCE_DIR}/test/LPI_output.txt.s 
        ${EXECUTABLE_OUTPUT_PATH}LPI_output-blsm.txt.s )
endif()
add_test(hdf5_1_small ${EXECUTABLE_OUTPUT_PATH}/beamLossPattern 
 ${CMAKE_CURRENT_SOURCE_DIR}/test/tracks2.h5 output-hd.txt
 ${CMAKE_CURRENT_SOURCE_DIR}/test/allapert_20080127.b1
 ${CMAKE_CURRENT_SOURCE_DIR}/test/SurveyWithCrossing_XP_inj.dat)
if(PYTHONINTERP_FOUND)
add_test(hdf5_2_small ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/comparekLPIs.py ${CMAKE_CURRENT_SOURCE_DIR}/test/LPI_output.txt.s 
        ${EXECUTABLE_OUTPUT_PATH}LPI_output-hd.txt.s )
endif()
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/test/tracks2-large.dat)
  add_test(large-dat_1 ${EXECUTABLE_OUTPUT_PATH}/beamLossPattern 
  ${CMAKE_CURRENT_SOURCE_DIR}/test/tracks2-large.dat output-datL.txt
  ${CMAKE_CURRENT_SOURCE_DIR}/test/allapert_20080127.b1
  ${CMAKE_CURRENT_SOURCE_DIR}/test/SurveyWithCrossing_XP_inj.dat)
  if(PYTHONINTERP_FOUND)
  add_test(large-dat_2 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/comparekLPIs.py ${CMAKE_CURRENT_SOURCE_DIR}/test/LPI_output-large.txt.s 
          ${EXECUTABLE_OUTPUT_PATH}LPI_output-datL.txt.s )
  endif()
endif()
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/test/tracks2-large.h5)
  add_test(large-hdf_1 ${EXECUTABLE_OUTPUT_PATH}/beamLossPattern 
  ${CMAKE_CURRENT_SOURCE_DIR}/test/tracks2-large.h5 output-hdfL.txt
  ${CMAKE_CURRENT_SOURCE_DIR}/test/allapert_20080127.b1
  ${CMAKE_CURRENT_SOURCE_DIR}/test/SurveyWithCrossing_XP_inj.dat)
  if(PYTHONINTERP_FOUND)
  add_test(large-hdf_2 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/comparekLPIs.py ${CMAKE_CURRENT_SOURCE_DIR}/test/LPI_output-large.txt.s 
          ${EXECUTABLE_OUTPUT_PATH}LPI_output-hdfL.txt.s )
  endif()
endif()
