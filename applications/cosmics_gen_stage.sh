#!/bin/bash
# inputs: #file_number #run #event
echo "Start Time: " `date +%d-%b-%Y\ %H:%M:%S`
echo "Entered MCP2_0 physics-book cosmics script:"

# check if files at each stage already exist, if they do then we can skip these parts when running
export SINGULARITYENV_check_corsikadb=$(ls | grep p_showers_*.db)
export SINGULARITYENV_check_gen=$(ls | grep prodcorsika_$1_$3_Gen.root)

# sinularity container doesnt work well with empty vars, so set to FileNotFound instead of checking empty
if [ -z $SINGULARITYENV_check_corsikadb ]; then SINGULARITYENV_check_corsikadb="FileNotFound"; fi
if [ -z $SINGULARITYENV_check_gen ]; then SINGULARITYENV_check_gen="FileNotFound"; fi

# print the status of the files
echo
echo "Status of files:"
echo "Corsika db: $SINGULARITYENV_check_corsikadb"
echo "Generation stage: $SINGULARITYENV_check_gen"

# if final file exists then we can exit the job without running anything
if [ $SINGULARITYENV_check_gen != "FileNotFound" ]; then 
  echo "Gen stage file exists, so this job must have finished."
  echo "exit 0"
  exit 0
fi

echo "------------------------------------------------------------------------"

# run python setup script
if [ $SINGULARITYENV_check_corsikadb == "FileNotFound" ]; then
   echo "python /lus/theta-fs0/projects/neutrinoADSP/sbnd_MCP2_0_fcls/setup_cosmics.py"
   python /lus/theta-fs0/projects/neutrinoADSP/sbnd_MCP2_0_fcls/setup_cosmics.py
fi

echo "------------------------------------------------------------------------"

start_time=`date +%s`
start_time_h=`date`

CONTAINER=/lus/theta-fs0/projects/datascience/cadams/serial_apps/singularity_slf7-balsam.sif

## launch singularity container
singularity run --no-home -B /lus:/lus -B /soft:/soft -B /projects:/projects $CONTAINER <<EOF
  # setup sbndcode
  echo "Setting up sbndcode:"
  source /lus/theta-fs0/projects/neutrinoADSP/sbndcode_MCP2.0/setup
  setup sbndcode v08_36_01_3_MCP2_0 -q e17:prof  
  echo "sbndcode setup complete."

  echo "------------------------------------------------------------------------" 

  # run generation stage
  if [ $SINGULARITYENV_check_gen == "FileNotFound" ]; then
     echo "lar -c prodcorsika_cosmics_proton_theta.fcl -n 1 -e $2:1:$3 -o prodcorsica_$1_$3_Gen.root"
     lar -c prodcorsika_cosmics_proton_theta.fcl -n 1 -e $2:1:$3 -o prodcorsica_$1_$3_Gen.root
  fi

  echo "------------------------------------------------------------------------"

  echo "Finished executing larsoft commands."

EOF

echo "Start time: $start_time_h"
echo "Run time: $(expr `date +%s` - $start_time) s"

# check whether job sucessful and set appropriate exit status
# existance of final state file means job ran sucessfully, perform clean-up of directory
exit_status=$(ls | grep "prodcorsica_$1_$3_Gen.root")

if [[ -z "$exit_status" ]]; then
  echo "The final file does not exist, job has FAILED..."
  echo "exit 1"
  echo "End Time: " `date +%d-%b-%Y\ %H:%M:%S`
  exit 1
elif [[ -n "$exit_status" ]]; then
  echo "Found final file, job has SUCCEEDED..."
  echo "Removing files from previous stages from directory"
  echo "rm p_showers*.db *hist*.root *RootOutput*.root *TFileService*.root"
  rm p_showers*.db *hist*.root RootOutput*.root *TFileService*.root
  echo "exit 0"
  echo "End Time: " `date +%d-%b-%Y\ %H:%M:%S`
  exit 0
else
  echo "Eh?! Whats this exit status?"
  echo "End Time: " `date +%d-%b-%Y\ %H:%M:%S`
  exit 2
fi




