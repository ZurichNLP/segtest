#!/bin/sh

bpe_d500_model=$segtest_dir/models/bpe-d500
working_dir=$segtest_dir/models/char
model_dir=$working_dir/model

mkdir -p $model_dir

# Copy model parameters from previous model
cat $bpe_d500_model/model/checkpoint | sed 's/bpe-d500/char/g' > $model_dir/checkpoint
cp $bpe_d500_model/model/model-390000.* $model_dir
sed -i 's/bpe-d500/char/g' $model_dir/model-390000.json
