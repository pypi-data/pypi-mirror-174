#!/bin/bash
# #SBATCH -p RM-shared
#SBATCH --mail-type=BEGIN
#SBATCH --nodes=1                # node count
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=16G                # total memory per node (4 GB per cpu-core is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --ntasks-per-node=2
#SBATCH --job-name jupyter
#SBATCH --output jupyter-log.txt
#SBATCH -t 18:00:00
# #SBATCH -A ibn200014p

## get tunneling info
XDG_RUNTIME_DIR=""
ipnport=$(shuf -i8000-9999 -n1)
ipnip=$(hostname -i)

## print tunneling instructions to jupyter-log-{jobid}.txt
echo -e "
    Copy/Paste this in your local terminal to ssh tunnel with remote
    -----------------------------------------------------------------
    ssh -N -L $ipnport:$ipnip:$ipnport caleb.ellington@ciai.mbzuai.ac.ae
    -----------------------------------------------------------------
    Then open a browser on your local machine to the following address
    ------------------------------------------------------------------
    localhost:$ipnport  (prefix w/ https:// if using password)
    ------------------------------------------------------------------
    "
## start an ipcluster instance and launch jupyter server
# cd $PROJECT
source /apps/local/conda_init.sh
conda activate jupyter
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
srun jupyter-notebook --NotebookApp.iopub_data_rate_limit=100000000000000 --no-browser --port=$ipnport --ip=$ipnip --NotebookApp.password='' --NotebookApp.token=''
