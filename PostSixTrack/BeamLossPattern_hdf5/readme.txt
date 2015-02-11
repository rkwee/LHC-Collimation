# to compile:

cd BeamLossPattern
mkdir build
cd build
# if already tried to compile and it failed, we must remove all old build files first!! 
rm -r *

source ~/gcc45-setup.sh 

cmake -DUSE_AFS=ON ../
# cmake -DWITH_OMPI=OFF ../

make