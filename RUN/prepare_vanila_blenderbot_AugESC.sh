python prepare.py \
    --config_name vanilla \
    --inputter_name vanilla \
    --data_name esconv \
    --knowledge sbert\
    --max_input_length 256 \
    --max_decoder_input_length 40 \
    --train_input_file ./_reformat/AugESC/combined_train.txt \
    --save_dir './DATA/vanilla.vanilla.esconv.sbert.AugESC'

#    --train_input_file ./_reformat/ \

