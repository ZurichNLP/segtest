#!/bin/sh

data_dir=$segtest_dir/test_suite_data
working_dir=$segtest_dir/models/bpe-d500
script_dir=$segtest_dir/scripts

# Learn a BPE model with 500 merges and reserved symbols for abstract forms
cat $data_dir/train.src $data_dir/train.trg > $data_dir/train.all

spm_train --input=$data_dir/train.all \
          --model_prefix=$working_dir/spm \
          --vocab_size=500 \
          --character_coverage=0.9999 \
          --model_type=bpe \
          --shuffle_input_sentence=True \
          --user_defined_symbols @INFIX_1@, @INFIX_2@, @INFIX_3@, @INFIX_4@, @CIRCUMFIX_1@, @CIRCUMFIX_2@, @CIRCUMFIX_3@, @CIRCUMFIX_4@, @VOWEL_HARMONY_1@, @VOWEL_HARMONY_2@, @VOWEL_HARMONY_3@, @VOWEL_HARMONY_4@, @FULL_REDUPLICATION@, @PARTIAL_REDUPLICATION@, @TRIPLICATION@, @COMPOUND_1@, @COMPOUND_2@, @COMPOUND_3@, @COMPOUND_4@, @COMPOUND_5@, @COMPOUND_6@, @COMPOUND_7@, @COMPOUND_8@, @COMPOUND_9@, @COMPOUND_10@

rm $data_dir/train.all

# Convert vocab to nematus format
python $script_dir/convert_spm_vocab.py $working_dir/spm.vocab
mv $working_dir/spm.vocab.json $working_dir/vocab.json

# Train data is not encoded because BPE-dropout is applied in separate training script
cp $data_dir/train.src $working_dir/train.src
cp $data_dir/train.trg $working_dir/train.trg

# Encode all remaining data
spm_encode --model=$working_dir/spm.model < $data_dir/dev.src > $working_dir/dev.src
spm_encode --model=$working_dir/spm.model < $data_dir/dev.trg > $working_dir/dev.trg
spm_encode --model=$working_dir/spm.model < $data_dir/compound.src > $working_dir/compound.src
spm_encode --model=$working_dir/spm.model < $data_dir/circumfix.src > $working_dir/circumfix.src
spm_encode --model=$working_dir/spm.model < $data_dir/infix.src > $working_dir/infix.src
spm_encode --model=$working_dir/spm.model < $data_dir/vowelharmony.src > $working_dir/vowelharmony.src
spm_encode --model=$working_dir/spm.model < $data_dir/reduplication.src > $working_dir/reduplication.src
