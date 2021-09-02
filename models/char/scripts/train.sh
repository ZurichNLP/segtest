#!/bin/sh

working_dir=$segtest_dir/models/char
model_dir=$working_dir/model
script_dir=$working_dir/scripts

# Train nematus model
python3 $nematus_home/nematus/train.py \
    --source_dataset $working_dir/train.src \
    --target_dataset $working_dir/train.trg \
    --dictionaries $working_dir/vocab.json \
                   $working_dir/vocab.json \
    --save_freq 30000 \
    --model $model_dir/model \
    --reload latest_checkpoint \
    --no_reload_training_progress \
    --model_type transformer \
    --embedding_size 512 \
    --state_size 512 \
    --tie_encoder_decoder_embeddings \
    --tie_decoder_embeddings \
    --loss_function per-token-cross-entropy \
    --label_smoothing 0.1 \
    --exponential_smoothing 0.0001 \
    --learning_rate 0.00001 \
    --optimizer adam \
    --adam_beta1 0.9 \
    --adam_beta2 0.98 \
    --adam_epsilon 1e-09 \
    --learning_schedule constant \
    --maxlen 1000 \
    --batch_size 256 \
    --token_batch_size 16384 \
    --max_tokens_per_device 4500 \
    --valid_source_dataset $working_dir/dev.src \
    --valid_target_dataset $working_dir/dev.trg \
    --valid_batch_size 120 \
    --valid_token_batch_size 4096 \
    --valid_freq 10000 \
    --valid_script $script_dir/validate.sh \
    --disp_freq 1000 \
    --sample_freq 0 \
    --beam_freq 0 \
    --beam_size 4 \
    --translation_maxlen 1000 \
    --normalization_alpha 0.6 \
    --patience 5 \
    --transformer_dropout_attn 0.2 \
    --finish_after 550000
