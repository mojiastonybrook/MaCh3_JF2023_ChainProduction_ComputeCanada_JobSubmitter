# MaCh3 Jonit Fit 2023 Chain Production on ComputeCanada with the JobSubmitter

The codes are used to create the necessary job scripts, run scripts and inputs for the massive production of MCMC chains with MaCh3, especially on the Cedar cluster of ComputeCanada. For efficiency we would like to have mulitple individual chains produced in parallel. For each chain there should be a specific configuration card assigned with it indicating the setups of that certain chain. A template of the config should be provided by the user in order to set up the common settings for the chains. As for the special setting of a certain chain, for example the save name of the final output file, it would be handled by the codes. The execuable from MaCh3 to produce a Markov chain would be called in a so-called RunScript; the RunScript are submitted to and executed by the cluster via a so-called SubmitScript. The templates of RunScript and SubmitScript should also be provided by the user and the contents would then be modified automaticaly by the codes according to the user-defined needs. The codes will ask the users about the setups for one batch of chain, prepare the needed files and submit the jobs to the cluster.

## How to use JobSubmitter on Cedar

- Set up an environmental variable `OUTDIR`, indicating the directory where you want the outputs of running MaCh3 to be saved. For example,
  ```
  export OUTDIR=/home/mojia/scratch/jointfit/SKonly
  ```
- Go to the MaCh3 install directory and soure the `setup.sh` there to set up the MaCh3 related environmental variables.

- In the JobSubmitter directory, check the contents in the subdirectory `SampleConfigs` to find the config cards for the samples. If no files are found, copy the corresponding files from MaCh3 install to this subdirectory.
   
- Load the python module
  ```
  module load python
  ```
- Run the python script and answer the prompt questions
  ```
  python LetsGo_03212023.py 
  ```
- The script would ask sevaral questions for the exact setups of the batch of the parallel chains. Here is an specific example for those settings with some breif explanations. In principle the users could change the settings according to their actual needs.

   1. > Job Name?: 
      >
      > skonly_batch_0
      
      The remote job name appears on slurm.
   2. > How many jobs?:
      >
      > 4
      
      The number of job arrays inside this batch.
      Slurm supports a feature of utilizing job array for repetitive submissions of one SubmitScript. With this, the same one SubmitScript would be handed to the cluster for the same number of times as the job arrays, each time with an automatic changed id for separation.

   3. > How many GPUs per job?:
      >
      > 4
      > 
      > How many execs per job?:
      >
      > 4
      >
      > How many threads per job?:
      >
      > 32

      The compute resource settings for the chains in one job array.

      `execs` means an individual Markov chain. Usually one GPU and 8 threads is assigned to one chain. In this example, in one job array there are 4 chains thus 4 GPUs and 32 threads intotal should be provided to this one job array.

   4. > How many steps per chain?:
      >
      > 1000000000  

      We want to run each chain as long as possible, so just put some infinitly large number here to make sure the chain not stopped when the job reach the time wall on the cluster

   5. > How many iterations:
      >
      > 4
      
      We want to run the chain as long as possible, but there is a time limit for the remote job. Thus we could break one chain into serval subchain, with the later one starting at the point where the previous one stops. Running one subchain is called an `iteration` here.

   6. > Executable to run? (Given in relative path to MaCh3 Install, e.g. ./bin/jointFit):
      >
      > ./AtmJointFit_Bin/JointAtmFit_CorrFDDet_Data
      
      The executables in MaCh3 
   7. > Base Config Name:
      >
      > AtmConfig_SKonly.cfg 

      Template for the configuration card. The specific setting in the template should be changed by the users according to the requirements of the fits that needs to be done.

   8. > Sample Config Direcotry:
      >
      > SampleConfigs

      Templates for the samples

   9. > Run Script Name:
      >
      > RunScript.sh
      
      Template for the run script. The run script will call the exectuabe above to start the computing process.

   10. > Submit script to run? (Given in relative path to $PWD, e.g. ./SubmitScript.sh):
       >
       > SubmitScript_CC.sh
       
       Template for the submission script. The submission script will ask the cluster the allocate the above computing resources and execute the run script. With job arrays, the submission script would repeat this process automatically.

    11. > Extra label string except for date to distinguish several trials in one day? (eg: trial_n) :
        >
        > batch_0
        
        A certain label to distinguish different batches of chains

    12. > Submit jobs to queue? (1 for yes, 0 for no):

        If yes, then the jobs would be submitted automatically after the files are prepared.

        If no, the files would be prepared but not submitted to the cluster. 

    13. > Continue? (0 for no, 1 for yes):
        
        If yes, the rest process would be done by the codes; if no, the codes stop here.
        
- Check the newly created the subdirectory.
