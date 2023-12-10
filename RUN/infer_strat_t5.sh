python infer.py \
    --config_name emp_dialog_t5 \
    --inputter_name emp_dialog_t5 \
    --data_name esconv \
    --knowledge_name sbert \
    --add_nlg_eval \
    --add_mi_analysis \
    --seed 13 \
    --load_checkpoint ./DATA/emp_dialog_t5.emp_dialog_t5.esconv.sbert/2023-11-21014333.0.0001.32.1gpu/epoch-13.bin \
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


# ./DATA/emp_dialog_t5.emp_dialog_t5.esconv.sbert/2023-10-31154507.3e-05.16.1gpu/epoch-9.bin \  # first trial
