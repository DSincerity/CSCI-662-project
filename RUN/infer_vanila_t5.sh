python infer.py \
    --config_name vanilla_t5 \
    --inputter_name vanilla_t5 \
    --data_name esconv \
    --knowledge_name sbert \
    --add_nlg_eval \
    --seed 13 \
    --load_checkpoint ./DATA/vanilla_t5.vanilla_t5.esconv.sbert/2023-11-22140153.3e-05.16.1gpu/epoch-1.bin \
    --fp16 false \
    --max_input_length 256 \
    --max_decoder_input_length 40 \
    --max_length 40 \
    --min_length 15 \
    --infer_batch_size 2 \
    --infer_input_file ./_reformat/ \
    --temperature 0.7 \
    --top_k 30 \
    --top_p 0.3 \
    --num_beams 1 \
    --repetition_penalty 1 \
    --no_repeat_ngram_size 3


#./DATA/vanilla_t5.vanilla_t5.esconv.sbert/2023-11-21232823.3e-05.64.1gpu/epoch-2.bin \
