#!/bin/sh

translations=$1

working_dir=$segtest_dir/models/char
script_dir=$working_dir/scripts

ref=dev.ref

# Compute BLEU on dev set
$script_dir/postprocess.sh < $translations | sacrebleu --force -q -w 2 -b $working_dir/$ref
