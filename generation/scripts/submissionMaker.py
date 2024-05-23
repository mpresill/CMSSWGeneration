import os
import fileinput

import subprocess
import re
import json
import sys


year    = "2018"
samples = [
#"aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WPlepWMhadJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WPhadZlepJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WMlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WPlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10",
#"aQGC_WPlepWPhadJJ_EWK_LO_SM_mjj100_pTj10"
"test2",
]

cwd = os.getcwd()
print "we are here: ", cwd
for sample in samples:
    print "sample: ",sample
    filepath = '/work/mpresill/nanov7_private_production/CMSSWGeneration/generation/output/{}_TuneCP5_MINIAOD_{}.txt'.format(sample,year)
    print "filepath: ", filepath
    directory = '{}_official/'.format(year)
    print "directory: ", directory #2017_official
    
    files = []
    cnt = 0
    with open(filepath) as fp:
       line = fp.readline()
       while line:
           print("Line {}: {}".format(cnt, line.strip()))
           files.append(line)
           line = fp.readline()
           cnt += 1
    # os.system('cd {}/'.format(directory))
    # print ( cnt )
    wrapperFile = '{}_official/wrapper.sh'.format(year)
    jdlFile     = '{}_official/submit.jdl'.format(year)
    #print "wrapperFile: ", wrapperFile # 2017_official/wrapper.sh
    #print "jdlFile: ", jdlFile         # 2017_official/submit.jdl
    #os.mkdir(directory+'wrappers')
    #os.mkdir(directory+'submitters')
    for i in range(cnt):
        #wrapperFile_new = '{}'.format(wrapperFile.replace(".sh","_"+str(i)+".sh"))
        #jdlFile_new = '{}'.format(jdlFile.replace(".jdl","_"+str(i)+".jdl"))
        wrapperFile_new = '{}'.format(wrapperFile.replace(".sh","_"+sample+"_"+str(i)+".sh"))
        jdlFile_new = '{}'.format(jdlFile.replace(".jdl","_"+sample+"_"+str(i)+".jdl"))
        filein = open('{}'.format(wrapperFile))
        fileout = open(wrapperFile_new,"wt")
        for line in filein:
            fileout.write(line.replace('{INPUT}', files[i]).replace('{NUMBER}', str(i)).replace('{SAMPLE}',sample))
        filein.close()
        fileout.close()

        filein = open('{}'.format(jdlFile))
        fileout = open(jdlFile_new,"wt")
        for line in filein:
            fileout.write(line.replace('{WRAPPER}', wrapperFile_new).replace('{STEP}', str(i)).replace('{FILE}',year+"_"+sample))
        filein.close()
        fileout.close()

#    os.chdir(directory)
    for i in range(cnt):
        os.system("condor_submit {}submit_{}_{}.jdl".format(directory,sample,str(i)))
        print "submitting...", "condor_submit {}submit_{}_{}.jdl".format(directory,sample,str(i))




    os.chdir(cwd)




