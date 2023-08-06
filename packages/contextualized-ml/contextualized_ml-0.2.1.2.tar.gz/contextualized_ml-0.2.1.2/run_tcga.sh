bash remote.sh push
# bash remote.sh run experiments/TCGA/train_tcga_notmad.py hallmarks_10_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_notmad.py hallmarks_25_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_notmad.py hallmarks_50_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_notmad.py hallmarks_100_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_notmad.py hallmarks_292_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_correlator.py hallmarks_10_dataset.pkl
bash remote.sh run experiments/TCGA/train_tcga_correlator.py hallmarks_25_dataset.pkl
bash remote.sh run experiments/TCGA/train_tcga_correlator.py hallmarks_50_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_correlator.py hallmarks_100_dataset.pkl
# bash remote.sh run experiments/TCGA/train_tcga_correlator.py hallmarks_292_dataset.pkl
bash remote.sh check
