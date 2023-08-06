#!/bin/bash

# These are specified in remote.sh, uncomment to run sbatch manually
# #SBATCH --job-name=name
# #SBATCH --output=results/%x_%j.log 
# #SBATCH --error=results/%x_%j.err

#SBATCH --nodes=1                # node count
#SBATCH --ntasks-per-node=1      # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=16G                # total memory per node (4 GB per cpu-core is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=200:00:00         # total run time limit (HH:MM:SS)

source /apps/local/conda_init.sh
conda activate ${1}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
srun python -u ${2} ${3} ${4}
