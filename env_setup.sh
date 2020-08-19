#!/bin/bash 


if [ $# -ne 1 ];
then
    echo "Please provide path to virtual env that you wish to create"
    exit 1
fi

env_path=$1

module swap PrgEnv-intel PrgEnv-gnu
module load cray-python
export CC=cc
export CXX=CC
export FC=ftn
export MPICC=cc
export MPICXX=CC

module load postgresql


source  $env_path//bin/activate
