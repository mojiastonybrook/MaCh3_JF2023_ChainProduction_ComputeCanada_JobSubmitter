import os
import sys
import subprocess
from datetime import datetime

def replaceText(File,oldText,newText):
    with open(File) as f:
        newText=f.read().replace(oldText,newText)
    with open(File,"w") as f:
        f.write(newText)

def main():
    print("\n")
    
    WorkDirectory = os.environ['PWD']
    
    try:
        MaCh3Install = os.environ['MACH3']
    except:
        print("MaCh3 install not found. Please source setup.sh in MaCh3 install or export $MACH3=/path/to/MACH3")
        quit()

    if (os.path.exists(MaCh3Install) == False):
        print("MaCh3 install not found. Given:"+MaCh3Install)
        quit()

    try:
        JobName = input("Job Name?: ")
    except:
        JobName = "MaCh3"
        
    try:
        nJobs = int(input("How many jobs?: "))
    except:
        print("Invalid number of jobs")
        quit()

    try:
        nGPUsPerJob = int(input("How many GPUs per job?: "))
    except:
        print("Invalid number of GPUs")
        quit()

    try:
        nExecsPerJob = int(input("How many execs per job?: "))
    except:
        print("Invalid number of execs per job")
        quit()        

    try:
        nThreads = int(input("How many threads per job?: "))
    except:
        print("Invalid number of threads")
        quit()

    try:
        nSteps = int(input("How many steps per chain?: "))
    except:
        print("Invalid number of steps")
        quit()

    if (nThreads == 0):
        print("\tDefaulting to use 1 thread")
        nThreads = 1
    
    try:
        nIterations = int(input("How many iterations: "))
    except:
        print("Invalid Iteration Number")
        quit()
        
    ExecName = ""
    try:
        ExecName = input("Executable to run? [Given in relative path to MaCh3 Install, e.g. ./bin/jointFit]: ")
    except:
        print("Invalid executable name")

    if ((os.path.exists(MaCh3Install+"/"+ExecName) == False) or (ExecName == "")):
        
        print("\tExecutable:"+ExecName+" not found in MaCh3 install:"+MaCh3Install)
        ExecName = "./AtmJointFit_Bin/JointAtmFit"
        if (os.path.exists(MaCh3Install+"/"+ExecName) == True):
            print("\tDefaulting to use: "+ExecName)
        else:
            print("Invalid executable name")
            quit()
        
    try:
        ConfigName = input("Base Config Name:")
    except:
        print("Invalid config name string")
        quit()

    if (os.path.exists(WorkDirectory+"/"+ConfigName) and (ConfigName != '')):
        ConfigName = WorkDirectory+"/"+ConfigName
    else:
        print("\tConfig: "+ConfigName+" not found in current working directory: "+WorkDirectory)
        ConfigName = WorkDirectory+"/Config.cfg"

        if (os.path.exists(ConfigName)):
            print("\tDefaulting to use: "+ConfigName)
        else:
            print("Not found valid config")
            quit()

    try:
        SampleConfigDir = input("Sample Config Direcotry:")
    except:
        print("Invalid sample config directory string")
        quit()

    if (os.path.exists(WorkDirectory+"/"+SampleConfigDir) and (SampleConfigDir != '')):
        SampleConfigDir = WorkDirectory+"/"+SampleConfigDir
    else:
        print("SampleConfigDir: "+SampleConfigDir+" not found in current working directory: "+WorkDirectory)
        SampleConfigDir = WorkDirectory+"/SampleConfigs/"

        if (os.path.exists(SampleConfigDir)):
            print("\tDefaulting to use: "+SampleConfigDir)
        else:
            print("Not found valid run script")
            quit()
            
    try:
        RunScriptName = input("Run Script Name:")
    except:
        print("Invalid run script name string")
        quit()

    if (os.path.exists(WorkDirectory+"/"+RunScriptName) and (RunScriptName != '')):
        RunScriptName = WorkDirectory+"/"+RunScriptName
    else:
        print("\tRunScript: "+RunScriptName+" not found in current working directory: "+WorkDirectory)
        RunScriptName = WorkDirectory+"/RunScript.sh"

        if (os.path.exists(RunScriptName)):
            print("\tDefaulting to use: "+RunScriptName)
        else:
            print("Not found valid run script")
            quit()
            
    try:
        SubmitScriptName = input("Submit script to run? [Given in relative path to $PWD, e.g. ./SubmitScript.sh]: ")
    except:
        print("Invalid submit script name")

    if ((os.path.exists(WorkDirectory+"/"+SubmitScriptName) == False) or (SubmitScriptName == "")):
        print("\tSubmitScript: "+SubmitScriptName+" not found in current working directory: "+WorkDirectory)

        SubmitScriptName = "./SubmitScript.sh"
        if (os.path.exists(WorkDirectory+"/"+SubmitScriptName)):
            print("\tDefaulting to use: "+SubmitScriptName)
        else:
            print("Not found valid SubmitScript")
    else:
        SubmitScriptName = WorkDirectory+"/"+SubmitScriptName


    try:
        ExtraLabel = input("Extra label string except for date to distinguish several trials in one day? [eg: trial_n] : ")
    except:
        print("Invalid answer")
        quit()
        
    if (ExtraLabel == ""):
        print("Setting label to be trial_0")
        ExtraLabel = "trial_0"
        
        
    try:
        OutDirectory = os.environ['OUTDIR']
    except:
        print("Output directory not found. Using current directory. If this is not acceptable, export OUTDIR=/path/to/output")
        OutDirectory = os.environ['PWD']

    try:
        SubmitJobs = int(input("Submit jobs to queue? [1 for yes, 0 for no]: "))
    except:
        print("Invalid answer")
        quit()
        
    print("\n\n")
    print("Summary: ---------")
    print("\tMaCh3 Install:"+MaCh3Install)
    print("\tNumber of Jobs:"+str(nJobs))
    print("\tNumber of GPUs per Job:"+str(nGPUsPerJob))
    print("\tNumber of Executables per Job:"+str(nExecsPerJob))
    print("\tNumber of Steps per Job:"+str(nSteps))
    print("\tNumber of Threads per Job:"+str(nThreads))
    print("\tNumber of Iterations:"+str(nIterations))
    print("\tExecutable:"+ExecName)
    print("\tBase Config:"+ConfigName)
    print("\tSample Config Directory:"+SampleConfigDir)
    print("\tBase RunScript:"+RunScriptName)
    print("\tBase SubmitScript:"+SubmitScriptName)
    print("\tOutput Directory:"+OutDirectory)

    if (SubmitJobs == 1):
        SubmitJobs = True
    else:
        SubmitJobs = False

    if (SubmitJobs):
        print("\tSubmitting jobs to queue")
    else:
        print("\tNot submitting jobs to queue")

    print("\n")
    Check = int(input("Continue? [0 for no, 1 for yes]: "))
    if (Check == 0):
        print("Quiting..")
        quit()

    ID = -1

    now = datetime.now()
    date_waterprint = now.strftime("%m%d%Y")
    
    for iIteration in range(nIterations):
        if (iIteration == 0):    
            StartFromFile = False
        else:
            StartFromFile = True

        FileNameBase_iIter = "Iter_"+str(iIteration)
        FileNameBase_m1_iIter = "Iter_"+str(iIteration-1)        

        ScriptDir_iIter = WorkDirectory+"/"+date_waterprint+"/"+ExtraLabel+"/Script_"+FileNameBase_iIter+"/"
        ScriptDir_Log_iIter = ScriptDir_iIter+"/SubmitLog"
        ScriptDir_Error_iIter = ScriptDir_iIter+"/SubmitError"
        ScriptDir_Output_iIter = ScriptDir_iIter+"/SubmitOutput"
        ScriptDir_Submit_iIter = ScriptDir_iIter+"/SubmitScript"
        
        MkdirCommand  = "mkdir -p "+ScriptDir_iIter
        os.system(MkdirCommand)
        MkdirCommand  = "mkdir -p "+ScriptDir_Log_iIter
        os.system(MkdirCommand)
        MkdirCommand  = "mkdir -p "+ScriptDir_Error_iIter
        os.system(MkdirCommand)
        MkdirCommand  = "mkdir -p "+ScriptDir_Output_iIter
        os.system(MkdirCommand)
        MkdirCommand  = "mkdir -p "+ScriptDir_Submit_iIter
        os.system(MkdirCommand)

        OutDir_iIter = OutDirectory+"/"+date_waterprint+"/"+ExtraLabel+"/Output_"+FileNameBase_iIter+"/"
        OutDir_m1_iIter = OutDirectory+"/"+date_waterprint+"/"+ExtraLabel+"/Output_"+FileNameBase_m1_iIter+"/"

        MkdirCommand = "mkdir -p "+OutDir_iIter
        os.system(MkdirCommand)

        JobName_iIter = JobName+"_"+str(iIteration)
        
        RunScriptName_iIter = ScriptDir_Submit_iIter+"/RunScript_Iter_"+str(iIteration)+".sh"
        SubmitScriptName_iIter = ScriptDir_Submit_iIter+"/SubmitScript_Iter_"+str(iIteration)+".sh"
        ScriptDirFileName_Error_iIter = ScriptDir_Error_iIter+"/SubmitError_Iter_"+str(iIteration)+".log"
        ScriptDirFileName_Log_iIter = ScriptDir_Log_iIter+"/SubmitLog_Iter_"+str(iIteration)+".log"

        OutputName_iIter_ID = []        
        OutputName_iIter_m1_ID = []
        ConfigName_iIter_ID = []
        ConsoleOutputName_iIter_ID = []

        for iExec in range(nExecsPerJob):
            OutputName_iIter_ID.append(OutDir_iIter+"MaCh3_Job_${ID}_Iter_"+str(iIteration)+"_Exec_"+str(iExec)+".root")
            OutputName_iIter_m1_ID.append(OutDir_m1_iIter+"MaCh3_Job_${ID}_Iter_"+str(iIteration-1)+"_Exec_"+str(iExec)+".root")
            ConfigName_iIter_ID.append(ScriptDir_Submit_iIter+"/Config_Job_${ID}_Iter_"+str(iIteration)+"_Exec_"+str(iExec)+".cfg")
            ConsoleOutputName_iIter_ID.append(ScriptDir_Output_iIter+"/ConsoleOutput_Job_${ID}_Iteration_"+str(iIteration)+"_Exec_"+str(iExec)+".log")
            
        for iJob in range(nJobs):

            OutputName_iIter = []
            OutputName_iIter_m1 = []
            ConfigName_iIter = []
            ConsoleOutputName_iIter = []

            for iExec in range(nExecsPerJob):
                OutputName_iIter.append(OutDir_iIter+"MaCh3_Job_"+str(iJob+1)+"_Iter_"+str(iIteration)+"_Exec_"+str(iExec)+".root")
                OutputName_iIter_m1.append(OutDir_m1_iIter+"MaCh3_Job_"+str(iJob+1)+"_Iter_"+str(iIteration-1)+"_Exec_"+str(iExec)+".root")
                ConfigName_iIter.append(ScriptDir_Submit_iIter+"/Config_Job_"+str(iJob+1)+"_Iter_"+str(iIteration)+"_Exec_"+str(iExec)+".cfg")
                ConsoleOutputName_iIter.append(ScriptDir_Output_iIter+"/ConsoleOutput_Job_"+str(iJob+1)+"_Iteration_"+str(iIteration)+"_Exec_"+str(iExec)+".log")
        
            for iExec in range(nExecsPerJob):
                Temp_ConfigName = WorkDirectory+"/Config_Temp.cfg"
                CopyCommand = "cp "+ConfigName+" "+Temp_ConfigName
                os.system(CopyCommand)
                            
                SedCommand = "sed -i 's|OUTPUTNAME.*|OUTPUTNAME = \""+OutputName_iIter[iExec]+"\"|' "+Temp_ConfigName
                os.system(SedCommand)
                
                if (StartFromFile):
                    SedCommand = "sed -i 's|STARTFROMPOS.*|STARTFROMPOS = true|' "+Temp_ConfigName
                else:
                    SedCommand = "sed -i 's|STARTFROMPOS.*|STARTFROMPOS = false|' "+Temp_ConfigName
                os.system(SedCommand)
                
                if (StartFromFile):
                    SedCommand = "sed -i 's|POSFILES.*|POSFILES = \""+OutputName_iIter_m1[iExec]+"\"|' "+Temp_ConfigName
                    os.system(SedCommand)
                
                SedCommand = "sed -i 's|NSTEPS.*|NSTEPS = "+str(nSteps)+"|' "+Temp_ConfigName
                os.system(SedCommand)
                
                SedCommand = "sed -i 's|ATMCONFIGDIR.*|ATMCONFIGDIR = \""+SampleConfigDir+"\"|' "+Temp_ConfigName
                os.system(SedCommand)

                SedCommand = "sed -i 's|BEAMCONFIGDIR.*|BEAMCONFIGDIR = \""+SampleConfigDir+"\"|' "+Temp_ConfigName
                os.system(SedCommand)
                
                mvCommand = "mv "+Temp_ConfigName+" "+ConfigName_iIter[iExec]
                print(mvCommand)
                os.system(mvCommand)

        Temp_RunScriptName = WorkDirectory+"/RunScript_Temp.sh"
        CopyCommand = "cp "+RunScriptName+" "+Temp_RunScriptName
        os.system(CopyCommand)
        
        replaceText(Temp_RunScriptName,"MACH3INSTALL",MaCh3Install)
        replaceText(Temp_RunScriptName,"NTHREADS",str(int(nThreads/nExecsPerJob)))
    
        for iExec in range(nExecsPerJob):
            iGPU = int(iExec/(nExecsPerJob/nGPUsPerJob))
            SedCommand = "sed -i -e '/^#INSERTJOB/abackground_pid_"+str(iExec)+"=$!' "+Temp_RunScriptName
            os.system(SedCommand)
            SedCommand = "sed -i -e '/^#INSERTJOB/a CUDA_VISIBLE_DEVICES=\""+str(iGPU)+"\" "+ExecName+" "+ConfigName_iIter_ID[iExec]+" > "+ConsoleOutputName_iIter_ID[iExec]+" &' "+Temp_RunScriptName
            os.system(SedCommand)
            
        for iExec in range(nExecsPerJob):
            SedCommand = "sed -i -e '/^#INSERTWAIT/await ${background_pid_"+str(iExec)+"} ' "+Temp_RunScriptName
            os.system(SedCommand)
            
        mvCommand = "mv "+Temp_RunScriptName+" "+RunScriptName_iIter
        os.system(mvCommand)
        
        Temp_SubmitScriptName = WorkDirectory+"/SubmitScript_Temp.sh"
        CopyCommand = "cp "+SubmitScriptName+" "+Temp_SubmitScriptName
        os.system(CopyCommand)
        
        replaceText(Temp_SubmitScriptName,"JOBNAME",JobName_iIter)
        replaceText(Temp_SubmitScriptName,"EXECUTABLENAME",RunScriptName_iIter)
        replaceText(Temp_SubmitScriptName,"SUBMITSCRIPTOUTPUT",ScriptDirFileName_Log_iIter)
        replaceText(Temp_SubmitScriptName,"ERRORFILE",ScriptDirFileName_Error_iIter)
        replaceText(Temp_SubmitScriptName,"ARRAY","1-"+str(nJobs))
        
        mvCommand = "mv "+Temp_SubmitScriptName+" "+SubmitScriptName_iIter
        os.system(mvCommand)
        
        if (SubmitJobs):
            SubmitCommand = "sbatch "
            if (StartFromFile):
                if (ID == -1):
                    print("Found ID == -1... argh")
                    quit()
                SubmitCommand += " --dependency=afterany:"+str(ID)+" "
                
            SubmitCommand += SubmitScriptName_iIter
            Return = subprocess.getoutput(SubmitCommand)
            ID = (Return.split(" "))[-1]
                                        
Version = sys.version_info[0]
if (Version != 3):
    print("Python3 required")
    quit()
    
main()
