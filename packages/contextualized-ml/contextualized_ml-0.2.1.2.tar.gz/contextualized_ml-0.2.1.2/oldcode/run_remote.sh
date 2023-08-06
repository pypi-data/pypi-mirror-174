SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
CURRPATH="$( pwd )"

EXPERIMENT="simulation"
SCRIPTNAME=${1}
BASEDIR="/home/caleb.ellington/ContextualizedCorrelator"

cd $SCRIPTPATH
bash push_code.sh
ssh caleb.ellington@ciai.mbzuai.ac.ae "sbatch \
	--job-name=${SCRIPTNAME} \
	--output=${BASEDIR}/experiments/${EXPERIMENT}/results/%x_%j.log \
	--error=${BASEDIR}/experiments/${EXPERIMENT}/results/%x_%j.err \
	${BASEDIR}/sbatch_remote.sbatch ${EXPERIMENT} ${SCRIPTNAME}"
cd $CURRPATH
