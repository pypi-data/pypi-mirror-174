bash remote.sh push
bash remote.sh run-torch experiments/TCGA/train_tcga_correlator.py hallmarks_10_dataset.pkl
bash remote.sh run-torch experiments/TCGA/paramscan_tcga_correlator.py hallmarks_10_dataset.pkl
bash remote.sh run-torch experiments/TCGA/train_tcga_correlator.py hallmarks_25_dataset.pkl
bash remote.sh run-torch experiments/TCGA/paramscan_tcga_correlator.py hallmarks_25_dataset.pkl
bash remote.sh run-tf experiments/TCGA/train_tcga_notmad.py hallmarks_10_dataset.pkl
bash remote.sh run-tf experiments/TCGA/paramscan_tcga_notmad.py hallmarks_10_dataset.pkl
bash remote.sh run-tf experiments/TCGA/train_tcga_notmad.py hallmarks_25_dataset.pkl
bash remote.sh run-tf experiments/TCGA/paramscan_tcga_notmad.py hallmarks_25_dataset.pkl
bash remote.sh check
