#!/bin/sh

data_dir=$segtest_dir/test_suite_data
bpe_d500_model=$segtest_dir/models/bpe-d500
working_dir=$segtest_dir/models/char
script_dir=$segtest_dir/scripts

# Modify BPE vocab with 500 merges to a character-level vocab
cp $bpe_d500_model/spm.model $working_dir
python $script_dir/create_char_level_vocab.py $bpe_d500_model/spm.vocab > $working_dir/spm.vocab

# Convert vocab to nematus format
python $script_dir/convert_spm_vocab.py $working_dir/spm.vocab
mv $working_dir/spm.vocab.json $working_dir/vocab.json

# Encode all data
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/train.src > $working_dir/train.src
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/train.trg > $working_dir/train.trg
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/dev.src > $working_dir/dev.src
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/dev.trg > $working_dir/dev.trg
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/compound.src > $working_dir/compound.src
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/circumfix.src > $working_dir/circumfix.src
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/infix.src > $working_dir/infix.src
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/vowelharmony.src > $working_dir/vowelharmony.src
spm_encode --model=$working_dir/spm.model --vocabulary=$working_dir/spm.vocab < $data_dir/reduplication.src > $working_dir/reduplication.src
