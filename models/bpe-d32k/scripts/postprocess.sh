#!/bin/sh

working_dir=$segtest_dir/models/bpe-d32k

# Reverse BPE
spm_decode --model=$working_dir/spm.model
