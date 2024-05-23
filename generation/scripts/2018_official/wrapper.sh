#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
#Working on nanoAOD step

echo "Opening CMSSW_10_2_22_ZV_EFT"
tar -xzvf CMSSW_10_2_22_ZV_EFT.tgz
rm CMSSW_10_2_22_ZV_EFT.tgz
cd CMSSW_10_2_22_ZV_EFT/src/
#export SCRAM_ARCH=slc6_amd64_gcc700
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"
cd ../../
date

# sed -i "s|file:SMP-RunIIAutumn18MiniAOD-00272.root|file:SMP-RunIIAutumn18MiniAOD-00272_${2}.root|g" -i SMP-RunIIAutumn18NanoAODv7-00274_1_cfg.py
# Impostare il percorso della proxy
export X509_USER_PROXY=/home/mpresill/.globus/x509_proxy
echo "Using proxy at: $X509_USER_PROXY"
# Verifica che il file della proxy sia presente
if [ ! -f "$X509_USER_PROXY" ]; then
    echo "Proxy file not found!"
    exit 1
fi
infile={INPUT}
echo ${infile}
xrdcp -f root://xrootd-cms.infn.it/${infile} SMP-RunIIAutumn18MiniAOD-00272.root
cmsRun SMP-RunIIAutumn18NanoAODv7-00274_1_cfg.py
mkdir -p /ceph/mpresill/privateProduction_aQGC_VBS_semileptonic_nanov7/aQGC_VVJJ_PrivateNanoProduction_2018/2018_{SAMPLE}/NanoAODv7/ ##check if crashes if the folder exists
cp -f SMP-RunIIAutumn18NanoAODv7-00274.root /ceph/mpresill/privateProduction_aQGC_VBS_semileptonic_nanov7/aQGC_VVJJ_PrivateNanoProduction_2018//2018_{SAMPLE}/NanoAODv7/SMP-RunIIAutumn18NanoAODv7-00274_{NUMBER}.root
#xrdcp -f SMP-RunIIAutumn18NanoAODv7-00274.root /ceph/mpresill/privateProduction_aQGC_VBS_semileptonic_nanov7/aQGC_VVJJ_PrivateNanoProduction_2018//2018_{SAMPLE}/NanoAODv7/SMP-RunIIAutumn18NanoAODv7-00274_{NUMBER}.root

rm SMP-RunIIAutumn18MiniAOD-00272_{NUMBER}.root SMP-RunIIAutumn18NanoAODv7-00274_1_cfg.py
rm -rf CMSSW_10_2_22_ZV_EFT 
date
