python prepare.py \
    --config_name strat \
    --inputter_name strat \
    --data_name esconv \
    --knowledge sbert\
    --train_input_file ./_reformat/ds_esconv_gpt/sbert_gpt/train.txt \
    --max_input_length 256 \
    --max_decoder_input_length 40 \
    --save_dir ./DATA/strat.strat.gpt
