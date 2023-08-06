ssh caleb.ellington@ciai.mbzuai.ac.ae "rm jupyter-log.txt || true && \
	sbatch jupyter.sbatch && \
	sleep 10 && \
	cat jupyter-log.txt"
