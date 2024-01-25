#!bin/bash

year=2017


samples=(
aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPlepWMhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPhadZlepJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WMlepZhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPlepZhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10
aQGC_WPlepWPhadJJ_EWK_LO_SM_mjj100_pTj10
)

for sample in ${samples[*]}; do

    # eosmkdir /store/group/lnujj/aQGC_VVJJ_PrivateNanoProduction_${year}/${year}_${sample}/NanoAODv7/
    # eosmkdir /store/group/lnujj/PrivateNanoLogs/${year}_${sample}_official/
    # # /aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
    # # dasgoclient -query="file dataset=/aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM" > aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10_TuneCP5_MINIAOD.txt
    # # echo "file dataset=/${sample}_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM"
    # # dasgoclient -query="file dataset=/${sample}_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" > ${sample}_TuneCP5_MINIAOD_${year}.txt   

    # # echo "file dataset=/${sample}_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM"
    # # dasgoclient -query="file dataset=/${sample}_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM" > ${sample}_TuneCP5_MINIAOD_${year}.txt   

    # echo "file dataset=/${sample}_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM"
    # dasgoclient -query="file dataset=/${sample}_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM" > ${sample}_TuneCP5_MINIAOD_${year}.txt 


    # cp -r ${year}_official ${year}_${sample}_official
    echo /eos/uscms/store/group/lnujj/aQGC_VVJJ_PrivateNanoProduction_${year}/${year}_${sample}/NanoAODv7
    ll /eos/uscms/store/group/lnujj/aQGC_VVJJ_PrivateNanoProduction_${year}/${year}_${sample}/NanoAODv7 | wc -l
done