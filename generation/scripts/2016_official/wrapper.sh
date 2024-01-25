#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
infile={INPUT}
echo ${infile}
xrdcp -f root://cmsxrootd.fnal.gov/${infile} SMP-RunIISummer16MiniAODv3-00473.root

#Working on nanoAOD step

echo "Opening CMSSW_10_2_22"
tar -xzvf CMSSW_10_2_22.tgz
rm CMSSW_10_2_22.tgz
cd CMSSW_10_2_22/src/
export SCRAM_ARCH=slc6_amd64_gcc700
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date
# sed -i "s|file:SMP-RunIISummer16MiniAODv3-00473.root|file:SMP-RunIISummer16MiniAODv3-00473_${2}.root|g" -i SMP-RunIISummer16NanoAODv7-00424_1_cfg.py
cmsRun SMP-RunIISummer16NanoAODv7-00424_1_cfg.py
xrdcp -f SMP-RunIISummer16NanoAODv7-00424.root root://cmseos.fnal.gov//store/group/lnujj/aQGC_VVJJ_PrivateNanoProduction_2016/2016_{SAMPLE}/NanoAODv7/SMP-RunIISummer16NanoAODv7-00424_{NUMBER}.root

rm SMP-RunIISummer16MiniAODv3-00473_{NUMBER}.root SMP-RunIISummer16NanoAODv7-00424_1_cfg.py
rm -rf CMSSW_10_2_22 
date
