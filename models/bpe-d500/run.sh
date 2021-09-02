#!/bin/sh

script_dir=$segtest_dir/models/bpe-d500/scripts

# Run the preprocessing and apply to data: learn a BPE model with 500 merges
bash $script_dir/preprocess.sh

# Train model with nematus and apply BPE-dropout after every epoch
bash $script_dir/train.sh

# Translate test sets with nematus
bash $script_dir/translate.sh
