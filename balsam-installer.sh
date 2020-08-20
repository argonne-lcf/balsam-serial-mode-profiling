#!/bin/bash
set -e 

if [ $# -ne 1 ];
then 
    echo "Please provide path to virtual env that you wish to create"
    exit 1
fi

env_path=$1
tmp_dir=/tmp/$USER/balsam-install

module swap PrgEnv-intel PrgEnv-gnu
module load cray-python
export CC=cc
export CXX=CC
export FC=ftn
export MPICC=cc
export MPICXX=CC

python -m venv $env_path
source $env_path/bin/activate

mkdir -p $tmp_dir
cd $tmp_dir

git clone https://github.com/mpi4py/mpi4py.git
cd mpi4py
pip install .
cd -

git clone https://github.com/balsam-alcf/balsam 
cd balsam
git checkout serial-mode-perf
pip install .

pip install python-dateutil

echo "Balsam install done."
echo "Use 'module load postgresql' to set up Postgres"
echo "If in doubt, delete ~/.balsam/settings.json to refresh Balsam settings"
