#!/bin/bash
#path_to_conda=$(conda info --base)
#source $path_to_conda"/etc/profile.d/conda.sh"
#conda activate py310
pkgName=$1
appName=$2
depth=$3
#pip3 list
#echo $pkgName $appName $depth
python3 run.py $pkgName $appName $depth