import os
import fileinput

year    = "2016"
samples = [
"aQGC_WMhadZlepJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_WPlepWMhadJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_ZlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_WPhadZlepJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_WPhadWMlepJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_WMlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_WPlepZhadJJ_EWK_LO_SM_mjj100_pTj10",
# "aQGC_WMlepWMhadJJ_EWK_LO_SM_mjj100_pTj10",
"aQGC_WPlepWPhadJJ_EWK_LO_SM_mjj100_pTj10"
]

cwd = os.getcwd()
for sample in samples:
    print "sample: ",sample
    filepath = '{}_TuneCP5_MINIAOD_{}.txt'.format(sample,year)
    directory = '{}_{}_official/'.format(year,sample)
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
    wrapperFile = 'wrapper.sh'
    jdlFile     = 'submit.jdl'
    os.mkdir(directory+'wrappers')
    os.mkdir(directory+'submitters')
    for i in range(cnt):
        wrapperFile_new = 'wrappers/{}'.format(wrapperFile.replace(".sh","_"+str(i)+".sh"))
        jdlFile_new = '{}submitters/{}'.format(directory,jdlFile.replace(".jdl","_"+str(i)+".jdl"))
        filein = open('{}{}'.format(directory,wrapperFile))
        fileout = open(directory+wrapperFile_new,"wt")
        for line in filein:
            fileout.write(line.replace('{INPUT}', files[i]).replace('{NUMBER}', str(i)).replace('{SAMPLE}',sample))
        filein.close()
        fileout.close()

        filein = open('{}{}'.format(directory,jdlFile))
        fileout = open(jdlFile_new,"wt")
        for line in filein:
            fileout.write(line.replace('{WRAPPER}', wrapperFile_new).replace('{STEP}', str(i)).replace('{FILE}',year+"_"+sample))
        filein.close()
        fileout.close()

    os.chdir(directory)
    for i in range(cnt):
        os.system("condor_submit submitters/submit_{}.jdl".format(str(i)))
    
    os.chdir(cwd)