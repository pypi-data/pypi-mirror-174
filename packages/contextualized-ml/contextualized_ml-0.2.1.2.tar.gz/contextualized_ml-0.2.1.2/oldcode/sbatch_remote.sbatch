#!/bin/bash
EXPERIMENT=${1}
SCRIPTNAME=${2}

#SBATCH --nodes=1                # node count
#SBATCH --ntasks-per-node=1      # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=16G                # total memory per node (4 GB per cpu-core is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=200:00:00         # total run time limit (HH:MM:SS)

source /apps/local/conda_init.sh
conda activate correlator
srun python -u ~/ContextualizedCorrelator/experiments/${EXPERIMENT}/${SCRIPTNAME}.py ${SCRIPTNAME}
