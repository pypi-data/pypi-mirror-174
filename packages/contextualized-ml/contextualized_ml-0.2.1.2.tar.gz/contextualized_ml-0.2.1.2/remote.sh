# Caleb Ellington, 5/8/2022
# Minimal interface for running/monitoring experiments on remote clusters from a local CLI

# 1.) Place remote.sh and remote.sbatch in the repo base directory
# 2.) Fill in the variables below with your remote user, domain, and the absolute paths for local and remote
# 3.) Push your code to the remote server: bash remote.sh push
# 3.1) Install your dependencies on your remote environment manually, or if you have a setup.py use: bash remote.sh install
# 4.) Run your experiment: bash remote.sh run <your script>
# 4.1.) Check your experiment: bash remote.sh check
# 5.) Retrieve any files in a directory labeled results/ using: bash remote.sh pull

USER="caleb.ellington"
SERVER="ciai.mbzuai.ac.ae"
REMOTE_CONDA_ENV="contextualized-torch"
LOCAL_REPO="/Users/calebellington/Workbench/Contextualized"
REMOTE_REPO="/home/caleb.ellington/Contextualized"


if [ ${1} == "push" ]; then
  echo "Syncing ${LOCAL_REPO} to ${USER}@${SERVER}:${REMOTE_REPO}"
  ssh ${USER}@${SERVER} "mkdir -p ${REMOTE_REPO}"
  rsync -azP --exclude-from='.rsync_ignore.txt' --delete ${LOCAL_REPO}/ ${USER}@${SERVER}:${REMOTE_REPO}/
fi


if [ ${1} == "install" ]; then
  echo "Installing ${USER}@${SERVER}:${REMOTE_REPO}/setup.py"
  ssh ${USER}@${SERVER} "cd ${REMOTE_REPO} && \
    source /apps/local/conda_init.sh && \
    conda activate ${REMOTE_CONDA_ENV} && \
    python -m pip install -e ."
fi


if [ ${1} == "run" ]; then
  echo "Running ${USER}@${SERVER}:${REMOTE_REPO}/${2}"
  SCRIPT_PATH="${REMOTE_REPO}/${2}" 
  SCRIPT_DIR=${SCRIPT_PATH%/*}
  SCRIPT_FILE=${SCRIPT_PATH##*/}
  SCRIPT_NAME=${SCRIPT_FILE%.*}
  ssh ${USER}@${SERVER} "cd ${SCRIPT_DIR} && \
    mkdir -p results && \
    sbatch --job-name=${SCRIPT_NAME} --output=${SCRIPT_DIR}/results/%x_%j.out ${REMOTE_REPO}/remote.sbatch ${REMOTE_CONDA_ENV} ${SCRIPT_FILE} ${3} ${4}"
fi


if [ ${1} == "check" ]; then
  echo "Checking ${USER}'s jobs on ${SERVER}"
  ssh ${USER}@${SERVER} "squeue -u ${USER}"
fi


if [ ${1} == "cancel" ]; then
  echo "Cancelling job ${USER} ${2} jobs on ${SERVER}"
  ssh ${USER}@${SERVER} "scancel ${2}"
fi


if [ ${1} == "pull" ]; then
  echo "Syncing ${USER}@${SERVER}:${REMOTE_REPO}/*/results/ to ${LOCAL_REPO}/*/results/"
  rsync -azP --include='results/**' --include='*/' --exclude='*' ${USER}@${SERVER}:${REMOTE_REPO}/ ${LOCAL_REPO}/
fi

