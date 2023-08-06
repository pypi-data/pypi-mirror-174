SYNCREPO="ContextualizedCorrelator"
rsync -azP --exclude-from='.rsync_ignore.txt' --delete ~/Workbench/${SYNCREPO}/ caleb.ellington@ciai.mbzuai.ac.ae:~/${SYNCREPO}
