#!/bin/sh

working_dir=$segtest_dir/models/bpe-d500
data_dir=$segtest_dir/test_suite_data
script_dir=$segtest_dir/scripts

for type in compound circumfix infix vowelharmony reduplication;
do
  echo "Accuracy on patterns of type:" $type;

  python $script_dir/evaluate.py -t $working_dir/$type.postprocessed \
                     -i $data_dir/$type.meta \
                     -s $data_dir/$type.scores \
                     -m $type \
                     -r surface;

  echo;

done
