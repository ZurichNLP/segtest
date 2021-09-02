#!/bin/sh

working_dir=$segtest_dir/models/char

# Reverse BPE
spm_decode --model=$working_dir/spm.model
