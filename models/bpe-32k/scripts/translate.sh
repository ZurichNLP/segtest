#!/bin/sh

working_dir=$segtest_dir/models/bpe-32k
model_dir=$working_dir/model
script_dir=$working_dir/scripts

checkpoint=model.best-valid-script

for type in compound circumfix infix vowelharmony reduplication;
do
  python3 $nematus_home/nematus/translate.py -m $model_dir/$checkpoint \
                                             -i $working_dir/$type.src \
                                             -o $working_dir/$type.out \
                                             --translation_maxlen 200 \
                                             -k 4 \
                                             -n 0.6 \
                                             -b 120 ;

  bash $script_dir/postprocess.sh < $working_dir/$type.out > $working_dir/$type.postprocessed;
done
