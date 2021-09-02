#!/bin/sh

script_dir=$segtest_dir/models/char/scripts

# Run the preprocessing and apply to data: get a character-level vocabulary
bash $script_dir/preprocess.sh

# Initialise from BPE model with 500 merges and BPE-dropout
bash $script_dir/init_from_bpe-d500.sh

# Train model with nematus
bash $script_dir/train.sh

# Translate test sets with nematus
bash $script_dir/translate.sh
