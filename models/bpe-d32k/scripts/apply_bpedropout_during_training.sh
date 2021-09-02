#!/bin/sh

working_dir=$segtest_dir/models/bpe-d32k

spm_encode --model=$working_dir/spm.model --output_format=sample_piece --alpha 0.1 < $working_dir/train.src > $working_dir/train.src.bpe &

spm_encode --model=$working_dir/spm.model --output_format=sample_piece --alpha 0.1 < $working_dir/train.trg > $working_dir/train.trg.bpe &

wait
