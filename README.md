# CMSSWGeneration

Updated: 31/01/2023

This repo is being updated to handle the reproduction of samples as an existing request of another sample. It is including also the case in which a singularity is needed. It is tested on lxplus. It assumes that you have the input gridpacks in an official directory.

Install this repo: ```git clone https://github.com/IreneZoi/CMSSWGeneration.git```

```
cd CMSSWGeneration/generation
voms-proxy-init -voms cms -rfc --valid 168:0
cp /tmp/x509up_XXXX /afs/cern.ch/user/U/USERNAME/private/x509up
```
NB: in the command above you need to change ```USERNAME``` & ```U``` based on your cern username and ```XXXX``` based on the output of the `voms-proxy-init` command.


## Download the correct CMSSW, architecture & config file for each year/step:

   * First put the correct flowlinks & links in Steps.json based on the request you are working with (in the example https://cms-pdmv.cern.ch/mcm/requests?page=0&dataset_name=WminusToLNuWminusTo2JJJ_dipoleRecoil_EWK_LO_SM_MJJ100PTJ10_TuneCP5_13TeV-madgraph-pythia8&shown=127 )
   
   * Then update the variable ```sobstituteMiniAOD``` in ```Downloader.py``` that is based on the request https://cms-pdmv.cern.ch/mcm/requests?page=0&dataset_name=WminusToLNuWminusTo2JJJ_dipoleRecoil_EWK_LO_SM_MJJ100PTJ10_TuneCP5_13TeV-madgraph-pythia8&shown=127 
   
   *   ```python Downloader.py -y 2016 -s lhe premix nanoAOD miniAOD```
   
This updates the Steps.json file.


## Generation 

Generate all the inputs for the job submission, assuming the gridpack is in the official repo:
```
python Generate.py -n MYOUTPUTDIR -y 2016 -gp /cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc700/13TeV/madgraph/V5_2.6.5/aQGC_semilep/aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10_slc6_amd64_gcc700_CMSSW_10_2_24_patch1_tarball.tar.xz -r False
cd outputdir/MYOUTPUTDIR
condor_submit submit.jdl
```

NB: It is a work in progress!!!


# generation scripts
In the `generation` folder there are two main scripts to generate with full sim given the `WLLJJ_WToLNu_EWK` flow.
You are encouraged to use them because of pathces and checks automatically inserted. 



## Old guide

Instructions on how to generate a private sample using crab in CMSSW 

Assumptions:

- LHE are available
- premixed library is available


Prepare to get premix library:

    voms-proxy-init -voms cms -rfc

LHE:

    example: /afs/cern.ch/user/g/govoni/myeos/samples/2019_EFT/SSeu/SM_limit/SSeu_SMlimit_results/1441466/SSeu_SMlimit_3/unweighted_events.lhe

# Generate2018

This folder allows to generate nanoAOD samples for 2018 year starting from a gridpack.

Open cmsconnect and go to `/local-scratch/<username>`

1. `git clone https://github.com/UniMiBAnalyses/CMSSWGeneration.git`

2. A `log` folder is necessary to save .log .err and .out files

    `mkdir log`

3. Open wrapper.sh L8 and change - if needed - with the suffix of your gridpack.

`gridpack_name="$1_<suffix of your gridpack>_tarball.tar.xz"`

4. Open submit.jdl L9 and change the first input, that is the absolute path to your gridpack. The name of the process must be replaced by `$(proc)`, for example:

`/local-scratch/<username>/gridpacks/$(proc)_slc7_amd64_gcc700_CMSSW_10_6_0_tarball.tar.xz`

5. To make scale and pdf weights available (this will be useful for nuisances at reco level), it is necessary to use CMSSW_10_6_20 sandbox. This means that you can create a CMSSW_10_6_20.tgz and then pass it as an input: 

```
cd Generate2018/input
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
scram b
cd ../..
tar -zcvf CMSSW_10_6_20.tgz CMSSW_10_6_20
```
    
You also need CMSSW_10_2_6.tgz, so let's repeat:
```
cd Generate2018/input
cmsrel CMSSW_10_2_6
cd CMSSW_10_2_6/src
cmsenv
scram b
cd ../..
tar -zcvf CMSSW_10_2_6.tgz CMSSW_10_2_6
```
6. The list of input files inside `input` folder should be now:
- SMP-RunIIAutumn18DRPremix-00050_1_cfg.py
- SMP-RunIIAutumn18DRPremix-00050_2_cfg.py
- SMP-RunIIAutumn18MiniAOD-00050_1_cfg.py
- SMP-RunIIAutumn18NanoAODv7-00058_1_cfg.py
- SMP-RunIIFall18wmLHEGS-00062_SM_1_cfg.py or SMP-RunIIFall18wmLHEGS-00062_EFT_1_cfg.py  
- CMSSW_10_6_20.tgz
- CMSSW_10_2_6.tgz

Open submit.jdl L9 and change the absolute path of the other 7 input files, for example

`/local-scratch/<username>/CMSSWGeneration/Generate2018/input/SMP-RunIIAutumn18DRPremix-00050_1_cfg.py`

One should choose between LHEGS for SM or EFT. The SM version is without dipoleRecoil and it should be used to validate the framework and in order to compare with old DAS samples which do not had this option. For newer sample it should be on, so please use the EFT version, regardless of what you are generating.

7. Create a folder to save all the nanoAOD files, for example `output`

    `mkdir output`

Open submit.jdl L10 and change the absolute path of your ouput folder (do not change `$(proc)/$(proc)_$(Cluster)_$(Step).root`), for example

`transfer_output_remaps = "SMP-RunIIAutumn18NanoAODv7-00058.root = /scratch/<username>/CMSSWGeneration/Generate2018/output/$(proc)/$(proc)_$(Cluster)_$(Step).root"`

8. Open submit.jdl L3 to change the number of events you want for each .root file.

`arguments = $(proc) <number of events>`

9. Open submit.sh L2 to change the number of .root files you want.

`sed -i "12s/.*/Queue <number of .root files> proc in ($1)/g" submit.jdl`

If your output folder has a different name, change also L3

`mkdir -p <your output folder>/$1`

10. Now everything is ready, you just need to run

    `./submit.sh <name of your process>`

where the name of the process is the one that appears in the gridpack.

The generation can last a few days, you can see its evolution using

    `condor_q`

# Generate2017

Example of outputs for 2017 production

    https://github.com/latinos/LatinoAnalysis/blob/master/NanoGardener/python/framework/samples/fall17_102X_nAODv5.py

    From the name of the sample:
    /GluGluHToWWTo2L2Nu_M125_13TeV_powheg2_JHUGenV714_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
    Get the different steps (backward) in the generation:
    
    NanoAOD
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17NanoAODv5-00331&page=0&shown=127
    
    MiniAOD 
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17MiniAODv2-02464&page=0&shown=127
    
    PreMix 
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17DRPremix-02533&page=0&shown=127
    
    wmLHE
    https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIIFall17wmLHEGS-01920&page=0&shown=127
    
Instructions:

    NanoAOD
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Running_on_various_datasets_from
    
    


    

Produce (from RunTheMatrix):

    # in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi  --conditions auto:phase1_2017_realistic -n 10 --era Run2_2017 --eventcontent FEVTDEBUG --relval 9000,50 -s GEN,SIM --datatier GEN-SIM --beamspot Realistic25ns13TeVEarly2017Collision --io TTbar_13UP17.io --python TTbar_13UP17.py --fileout file:step1.root  --nThreads 8 > step1_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1
    
    
    #    in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py step2  --datamix PreMix --conditions auto:phase1_2017_realistic --pileup_input das:/RelValPREMIXUP17_PU25/CMSSW_10_6_0-PU25ns_106X_mc2017_realistic_v3-v1/PREMIX --era Run2_2017 --procModifiers premix_stage2 -s DIGI:pdigi_valid,DATAMIX,L1,DIGI2RAW,HLT:@relval2017 --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --eventcontent FEVTDEBUGHLT --io DIGIPRMXUP17_PU25_RD.io --python DIGIPRMXUP17_PU25_RD.py -n 100  --filein  file:step1.root  --fileout file:step2.root  --nThreads 8 > step2_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1
    
    
    #    in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py step3  --conditions auto:phase1_2017_realistic -n 10 --era Run2_2017 --eventcontent RECOSIM,MINIAODSIM,DQM --runUnscheduled  --procModifiers premix_stage2 -s RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT,VALIDATION:@standardValidationNoHLT+@miniAODValidation,DQM:@standardDQMFakeHLT+@miniAODDQM --datatier GEN-SIM-RECO,MINIAODSIM,DQMIO --io RECOPRMXUP17_PU25.io --python RECOPRMXUP17_PU25.py --filein  file:step2.root  --fileout file:step3.root  --nThreads 8 > step3_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1
    
    
    #    in: /afs/cern.ch/work/a/amassiro/ECAL/SIM/ToRebase/CMSSW_11_0_X_2019-10-06-2300/src dryRun for 'cd 250202.172_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25
    cmsDriver.py step4  --conditions auto:phase1_2017_realistic -s HARVESTING:@standardValidationNoHLT+@standardDQMFakeHLT+@miniAODValidation+@miniAODDQM --filetype DQM --geometry DB:Extended --era Run2_2017 --mc  --io HARVESTUP17_PU25.io --python HARVESTUP17_PU25.py -n 100  --filein file:step3_inDQM.root --fileout file:step4.root  > step4_TTbar_13UP17+TTbar_13UP17+DIGIPRMXUP17_PU25_RD+RECOPRMXUP17_PU25+HARVESTUP17_PU25.log  2>&1

    

Where:

    /home/amassiro/Cern/Code/UniMiB/CMSSWGeneration
    
    /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Generation
    
    
-------------

# UL2020 SMEFTsim gridpack generation

In order to generate gradpacks for the LHE production stage one can take inspiration from https://github.com/GiacomoBoldrini/cmsgen .
The repo contains cards to produce gridpacks for inclusive WW with EFT contributions via SMEFTsim madgraph model.
The ReadMe describes the steps to produce gridpacks for the UL2020 campaign. For different campaigns or production one should carefully choose which branch of the genproduction to clone (UL2019 branch has mg 261 while master branch, as of  28/01/2020, has mg 265).
    
    
