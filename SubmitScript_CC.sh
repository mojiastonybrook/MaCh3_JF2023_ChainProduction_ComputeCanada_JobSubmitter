#!/bin/bash
#SBATCH --mail-user=mo.jia@stonybrook.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=JOBNAME
#SBATCH --output=SUBMITSCRIPTOUTPUT
#SBATCH --error=ERRORFILE
#SBATCH --account=rpp-blairt2k
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:v100l:4
#SBATCH --time=72:00:00
#SBATCH --mem=88G
#SBATCH --array=ARRAY

srun EXECUTABLENAME
