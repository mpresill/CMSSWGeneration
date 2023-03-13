import glob
import subprocess
from sys import argv
import os
import sys
from random import randint
import argparse 

def findLatestSubmit(folder,jdlfile):
    submit = glob.glob("output/{}/{}".format(folder,jdlfile))
    submitIds = list(map(lambda k: k.split("/")[-1].split(".")[0].split("submit")[1], submit))
    if len(submitIds)==1:
        return 1
    ids = sorted(list(filter(lambda k: k!='', submitIds)))
    ids = sorted(list(map(lambda k: int(k), ids)))
    print(ids[-1]+1)
    return ids[-1]+1


parser = argparse.ArgumentParser()
parser.add_argument("-d","--directory", help="Name for the generation, i.e. directory location on eos & output log" , required=True)
parser.add_argument("-y","--year", help="Year" , required=True)
parser.add_argument("-n","--njobs", help="Number of jobs", default=-1,type=int)
parser.add_argument("-j","--jdlfile", help="jdl file used for submission", default="submit.jdl")
parser.add_argument("-s","--step", help="mini or nano", default="mini")
args = parser.parse_args()

folder = args.directory.replace("/","")
print ("folder ",folder)

jdlfile = args.jdlfile
print " the jdlfile to be used is ",jdlfile

year=args.year
rootpath="output/{}/root/*.root".format(folder)
if "fnal" in os.uname()[1]:
    rootpath="/eos/uscms/store/group/lnujj/aQGC_VVJJ_Private_Production_{}/{}/".format(args.year,folder)
    if args.step == "mini":
        rootpath+="*MiniAOD*.root"
    elif args.step == "nano":
        rootpath+="*NanoAOD*.root"
    else:
        print "unknown step ",args.step
        sys.exit()
        
        
logpath="output/{}/log/*out*".format(folder)

print("root files path ",rootpath)
print("log files path ", logpath)

done = glob.glob(rootpath)
str_done = list(map(lambda k: k.split("/")[-1].split(".")[0].split("_")[-1], done))
done = list(map(int,str_done))
done = sorted(done)
print (" done ",set(done))
print (" number of done ",len(done))

finished = glob.glob(logpath)
str_finished = list(map(lambda k: k.split("/")[-1].split(".")[-1].split("_")[-1], finished))
finished = list(map(int,str_finished))
finished = sorted(finished)
print(" finished files ",set(finished))
print(" nunmber of finished ",len(finished))

missing_out = list(set(finished).difference(set(done)))
print("missing root files list from the out files ",sorted(missing_out))
print("overall the number of missing files is ",len(missing_out))

missing_dumb = list(set(sorted(done)).difference(set(finished))) 
print("List of the files for which I have the final root files but no out/err because still running for no reason!! ",sorted(missing_dumb))
print("overall the number of missing files is ",len(missing_dumb))

missing_tot = []
nfiles = -1
try:
    nfiles = args.njobs
except:
    nfiles = 0

if nfiles >0:
    expectedFiles = []
    for n in range(0,nfiles):
        expectedFiles.append(n)
        
    missing_tot = list(set(sorted(expectedFiles)).difference(set(done))) 
    print("List of the files I know are missing because I know the number of expected root files",sorted(missing_tot))
    print("overall the number of missing files is ",len(missing_tot))




if len(missing_out) ==0 and len(missing_tot) !=0 or len(list(set(sorted(done)).difference(set(finished)))) ==0:
    missing = missing_tot
elif len(missing_tot)> len(missing_out):
    missing = missing_tot
else:
    missing = missing_out

with open("output/{}/{}".format(folder,jdlfile)) as file:
    txt = file.read()
newTxt = txt.replace("$(Step)", "$(mystep)")
newTxt =  list(filter(lambda k: "queue" not in k.lower(), newTxt.split('\n')))
newTxt.append("Queue proc, mystep from (")
newTxt.append('\n'.join(['\t{}, {}'.format(folder, n) for n in missing]))
newTxt.append(")")
newTxt = '\n'.join(newTxt)
submitId = findLatestSubmit(folder,jdlfile)
with open("output/{}/submit{}.jdl".format(folder, submitId), "w") as file:
    file.write(newTxt)

txt = "#!/bin/bash\n"
for miss in missing:
    txt += "rm log/*_{}\n".format(miss)
txt += "condor_submit submit{}.jdl\n".format(submitId)
with open("output/{}/resubmit.sh".format(folder),"w") as file:
    file.write(txt)
p = subprocess.Popen("chmod +x output/{}/resubmit.sh".format(folder), shell=True)
p.wait()
