# MaCh3 Jonit Fit 2023 Chain Production on ComputeCanada with the JobSubmitter

The codes are used to create the necessary job scripts, run scripts and inputs for the massive production of MCMC chains with MaCh3, especially on the Cedar cluster of ComputeCanada. For efficiency we would like to have mulitple individual chains produced in parallel. For each chain there should be a specific configuration card assigned with it indicating the setups of that certain chain. A template of the config should be provided by the user in order to set up the common settings for the chains. As for the special setting of a certain chain, for example the save name of the final output file, it would be handled by the codes. The execuable from MaCh3 to produce a Markov chain would be called in a so-called RunScript; the RunScript are submitted to and executed by the cluster via a so-called SubmitScript. The templates of RunScript and SubmitScript should also be provided by the user and the contents would then be modified automaticaly by the codes according to the user-defined needs. The codes will ask the users about the setups for one batch of chain, prepare the needed files and submit the jobs to the cluster.

## How to use JobSubmitter on Cedar

- Set up an environmental variable `OUTDIR`, indicating the directory where you want the outputs of running MaCh3 to be saved. For example,
  ```
  export OUTDIR=/home/mojia/scratch/jointfit/SKonly
  ```
- Load the python module   
