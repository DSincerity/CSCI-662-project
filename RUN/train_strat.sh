python train.py \
    --config_name strat \
    --inputter_name strat \
    --data_name esconv \
    --knowledge_name sbert \
    --seed 13 \
    --max_input_length 256 \
    --max_decoder_input_length 40 \
    --train_batch_size 16 \
    --gradient_accumulation_steps 1 \
    --eval_batch_size 64 \
    --learning_rate 3e-5 \
    --num_epochs 5 \
    --warmup_steps 100 \
    --fp16 false \
    --loss_scale 0.0 \
    --pbar true

#--eval_input_file ./_reformat/ \
