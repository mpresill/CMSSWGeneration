import argparse 
import json
import sys
import os
import subprocess
from random import randint
import glob
import shutil

def create_CMSSW_tar(release, scram):
    print " --------------- release ",release," scram ",scram
    script  = "#!/bin/bash\n"

    script += "export SCRAM_ARCH={} \n".format(scram)
    script += "source /cvmfs/cms.cern.ch/cmsset_default.sh\n"
    script += "cd data/CMSSWs\n"
    script += "scram p {}\n".format(release)
    script += "cd {}/src\n".format(release)
    script += "eval `scramv1 runtime -sh`\n"
    if release =="CMSSW_10_2_22":
        #FIXME patch with giorgiopizz:
        script += "git cms-init\n"
        script += "git cms-merge-topic giorgiopizz:patch_10_2_22_nanoAOD_reweight\n"
    script += "scram b\n"
    script += "cd ../..\n"
    script += "tar -zcf {}.tgz {}\n".format(release, release)
    script += "rm -rf {}\n".format(release)
    nameTmpScript = "script_{}.sh".format(randint(100000,900000))
    with open(nameTmpScript, "w") as file:
        file.write(script)
    process = subprocess.Popen("chmod +x {}; ./{}; rm {}".format(nameTmpScript,nameTmpScript,nameTmpScript), shell=True)
    process.wait()

def generate(name, year, gridpack, removeOldRoot, dipoleRecoil, events, jobs, doBatch):
    with open("Steps.json") as file:
        Steps = json.load(file) 

    if not os.path.isfile(os.path.expanduser(gridpack)):
        print(gridpack)
        if not os.path.isfile("~"+str(gridpack[1:])):
            print("Gridpack path is not correct")
            return

    totalYears = ["2018", "2017", "2016"]
    if year not in totalYears:
        print("Year not valid")
        print("Valid years are: {}".format(", ".join(totalYears)))
        return
    
    totalSteps = ["lhe", "premix", "miniAOD", "nanoAOD"]

    cmssws = []
    scrams = []
    # print(Steps[year].keys())
    for k in totalSteps:
        cmssws.append(Steps[year][k]['release'])
        scrams.append(Steps[year][k]['SCRAM_ARCH'])
    cmssws.append('CMSSW_10_2_22')
    scrams.append('slc7_amd64_gcc700')
    print cmssws[0],cmssws[-1]
    print scrams[0],scrams[-1]
    print cmssws
    print scrams
    #cmssws = list(set(cmssws))
    #scrams = list(set(scrams))
    print(cmssws)

    for cmssw,scram in zip(cmssws,scrams):
        print cmssw,scram
    #for i in range(len(cmssws)):
        #cmssw = cmssws[i]
        #print scrams[i]
        #scram = scrams[i]
        if not os.path.isfile("data/CMSSWs/{}.tgz".format(cmssw)):
            print("Should create CMSSW tgz for release {}".format(cmssw))
            create_CMSSW_tar(cmssw, scram)


    if os.path.isdir("output/"+name):
        print("Dir with name: {} already present, can't create directory if they exist in python2 (blame Giacomo)".format(name))
        return
    os.makedirs("output/{}/root".format(name))
    os.makedirs("output/{}/log".format(name))




    
    fileToTransfer = [os.path.abspath(gridpack)]
    inputsCfg = glob.glob("data/input_{}/*.py".format(year))
    inputsCfg = list(map(lambda k: os.path.abspath(k), inputsCfg))
    fileToTransfer.extend(inputsCfg)
    print " inputsCfg ",inputsCfg
    print " year ",year
    print glob.glob("data/input_{}/*Nano*.py".format(year))
    outputFile = glob.glob("data/input_{}/*Nano*.py".format(year))[0].split("/")[-1].split("_1_")[0]
    for cmssw in cmssws:
        fileToTransfer.append(os.path.abspath(glob.glob("data/CMSSWs/{}.tgz".format(cmssw))[0]))


    jdl = "Universe = vanilla \n"
    if 'slc6' in Steps[year][k]['SCRAM_ARCH']:
         jdl += '+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel6" \n'
         jdl += 'Requirements = HasSingularity \n'
    jdl += "Executable = wrapper.sh\n"
    jdl += "arguments = $(proc) {}\n".format(events)
    jdl += "request_cpus = 8 \n"
    jdl += "should_transfer_files = YES\n"
    jdl += "Error = log/$(proc).err_$(Step)\n"
    jdl += "Output = log/$(proc).out_$(Step)\n"
    jdl += "Log = log/$(proc).log\n"
    jdl += "transfer_input_files = {}\n".format(", ".join(fileToTransfer))
    jdl += 'transfer_output_remaps = "{}.root = {}/$(proc)_$(Cluster)_$(Step).root"\n'.format(outputFile, os.path.abspath("output/{}/root".format(name)))
    jdl += "when_to_transfer_output = ON_EXIT\n"
    jdl += "Queue {} proc in ({})\n".format(jobs, name)

    with open("output/{}/submit.jdl".format(name), "w") as file:
        file.write(jdl)
    

    wrapper =  "#!/bin/bash\n"
    wrapper += 'echo "Starting job on " `date` #Date/time of start of job\n'
    wrapper += 'echo "Running on: `uname -a`" #Condor job is running on this node\n'
    wrapper += 'echo "System software: `cat /etc/redhat-release`" #Operating System on that node\n'
    wrapper += 'source /cvmfs/cms.cern.ch/cmsset_default.sh\n'

    openCMSSW = ""
    
    donePremixFirst = False
    totalSteps.insert(1, "premix")
    #print " --------------- commented premix!!!!! ------------------ "
    filesToRemove = [gridpack.split("/")[-1]]
    for k in totalSteps:
        wrapper += "#Working on {} step\n\n".format(k)
        file = list(filter(lambda j: k.lower() in j.lower(), inputsCfg))[0].split("/")[-1]
        if k == "premix":
            if not donePremixFirst:
                if "_2_" in file:
                    # should first run premix _1_
                    file = file[:-8]+"1_cfg.py"
                donePremixFirst = True
            else:
                if "_1_" in file:
                    # now should run premix _2_
                    file = file[:-8]+"2_cfg.py"
            
        if Steps[year][k]['release'] != openCMSSW:
            if openCMSSW != "":
                wrapper += "rm -rf {} \n".format(openCMSSW)
            wrapper += 'echo "Opening {}"\n'.format(Steps[year][k]['release'])
            wrapper += 'tar -xzvf {}.tgz\n'.format(Steps[year][k]['release'])
            wrapper += 'rm {}.tgz\n'.format(Steps[year][k]['release'])
            wrapper += 'cd {}/src/\n'.format(Steps[year][k]['release'])
            #if 'slc6' in Steps[year][k]['SCRAM_ARCH']: 
            #    print " ADDING SINGULARITY!!!!!"
            #    wrapper += "cmssw-slc6-condor \n"
            wrapper += 'export SCRAM_ARCH={}\n'.format(Steps[year][k]['SCRAM_ARCH'])
            wrapper += 'scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile\n'
            wrapper += 'eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers\n'
            wrapper += 'echo $CMSSW_BASE "is the CMSSW we have on the local worker node"\n'
            wrapper += 'cd ../../\n'
            openCMSSW = Steps[year][k]['release']
        print " -------------     DOING SUBSTITUTIONS!!!!!!!!"    
        if k == 'lhe':
            print " **** lhe time!!! ",gridpack," ",file
            #wrapper += "sed -i 's#^.*tarball.tar.xz.*$#    args = cms.vstring(\"./{}\"),#' -i {}\n".format(gridpack.split("/")[-1], file)
            wrapper += "sed -i 's#^.*tarball.tar.xz.*$#    args = cms.vstring(\"./{}\"),#' -i {}\n".format(gridpack, file)
            wrapper += 'sed -i "s/^.*nEvents = .*$/    nEvents = cms.untracked.uint32({}),/g" -i {}\n'.format(events, file)
            # if dipoleRecoil:
            #     wrapper += "sed '/^.*pythia8CP5Settings[^=]*=.*/i \ \ \ \ \ \ \ \ processParameters = cms.vstring(\"SpaceShower:dipoleRecoil = on\"),' {} -i\n".format(file)
        wrapper += "date\n"
        wrapper += "cmsRun {}\n".format(file)
        if removeOldRoot:
            if k == "lhe":
                filesToRemove.append(file.split("_")[0]+".root")
                filesToRemove.append(file.split("_")[0]+"_inLHE.root")
                
            elif k == "premix" and "_1_" not in file:
                filesToRemove.append(file.split("_")[0]+".root")
                filesToRemove.append(file.split("_")[0]+"_0.root")
            elif k == "miniAOD":
                filesToRemove.append(file.split("_")[0]+".root")
        wrapper += "\n\n"
    wrapper += "rm {}\n".format(" ".join(filesToRemove))
    wrapper += "rm -rf {} *py\n".format(openCMSSW)
    wrapper += "date\n"

    with open("output/{}/wrapper.sh".format(name), "w") as file:
        file.write(wrapper)



    process = subprocess.Popen("chmod +x output/{}/wrapper.sh".format(name), shell=True)
    process.wait()
    if (doBatch==1):
        process = subprocess.Popen('cd output/{}; condor_submit submit.jdl; cd -'.format(name), shell=True)
        process.wait()

def helperJsonParse(Samples, sample):
    params = []
    paramsD = {
        "removeOldRoot": True,
        "dipoleRecoil": True,
        "events": 2500,
        "jobs": 400,
        "doBatch": 0,
    }
    if not sample in Samples.keys():
        print("Sample {} not present in Samples.json".format(sample))
        return True, []
    required_params = ["year", "gridpack"]
    for p in required_params:
        if p not in Samples[sample].keys() or Samples[sample][p] =="":
            print("{} not present in Samples.json dict for {}".format(p, sample))
            return True, []
        paramsD[p] = Samples[sample][p]
    
    optional_params = ["removeOldRoot", "dipoleRecoil", "events", "jobs", "doBatch"]
    for p in optional_params:
        if p in Samples[sample].keys():
            paramsD[p] = Samples[sample][p]

    for p in required_params + optional_params:
        params.append(paramsD[p])
    return False, params




if __name__ == "__main__":
    argsT = sys.argv[1:]
    #by default using Samples.json, might specify which samples of Samples to use with -s SAMPLE_NAME1 SAMPLE_NAME2 ... 
    if len(argsT)==0 or argsT[0]=='-s':
        # use Samples.json
        print("Using Samples.json")
        with open("Samples.json") as file:
            Samples = json.load(file)

        if len(argsT)>1:
            samples_to_generate = argsT[1:]
        elif len(argsT)==0:
            samples_to_generate = list(filter(lambda k: not os.path.isdir("output/"+k), Samples.keys()))
        else:
            print("Invalid syntax, use -s SAMPLE_NAME1 SAMPLE_NAME2 (specify at least one sample)")
            sys.exit(-1)
        print("Generating samples: {}".format(", ".join(samples_to_generate)))
        for sample in samples_to_generate:
            print("\n\nNow working on sample {}\n\n".format(sample))
            skip, params = helperJsonParse(Samples, sample)
            if skip:
                continue
            print("Generating with params: {}".format([sample]+params))
            generate(*([sample]+params))


    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("-n","--name", help="Name for the generation, will be used for creating directories" , required=True)
        parser.add_argument("-y","--year", help="Year" , required=True)
        parser.add_argument("-gp","--gridpack", help="Path to gridpack", required=True)
        parser.add_argument("-r","--removeOldRoot", help="Option to remove intermediate root files (inLHE, miniAOD...), default = True", default=True)
        parser.add_argument("-dr","--dipoleRecoil", help="Whether to use dipole recoil in pythia, default = True", default=True)
        parser.add_argument("-e","--events", help="Number of events per file", default=2500)
        parser.add_argument("-j","--jobs", help="Number of jobs", default=400)
        parser.add_argument("-b","--doBatch", help="Wheter to submit or not (--doBatch=1)", default=0)
        args = parser.parse_args(argsT)
        generate(args.name, args.year, args.gridpack, args.removeOldRoot, args.dipoleRecoil, args.events, args.jobs, args.doBatch)
