#!/bin/sh

working_dir=$segtest_dir/models/bpe-d500

# Reverse BPE
spm_decode --model=$working_dir/spm.model
