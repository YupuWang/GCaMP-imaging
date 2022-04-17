#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=2000
#SBATCH --job-name=Myjob
#SBATCH --output=Myjob-%j.out
#SBATCH --error=Myjob-%j.err

module load <python> 

python preSelectMoviesNMJ.py

echo "job finished at 'date'"

