SYNCREPO="ContextualizedCorrelator"
rsync -azP --include='results/*' --include='*/' --exclude='*' caleb.ellington@ciai.mbzuai.ac.ae:~/${SYNCREPO}/ ~/Workbench/${SYNCREPO}
