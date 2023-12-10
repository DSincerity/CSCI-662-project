top_k_list="10 20 30"
temperature_list="0.01 0.5 0.7 0.99"
top_p_list="0.3 0.5 0.7"
num_beams_list="1 2"
# --top_k 0 \
# --top_p 0.9 \

for top_k in $top_k_list
do
    for temperature in $temperature_list
    do
        for top_p in $top_p_list
        do
            for num_beams in $num_beams_list
            do
                echo "top_k: $top_k, temperature: $temperature, top_p: $top_p, num_beams: $num_beams"
                python infer.py \
                    --config_name strat \
                    --inputter_name strat \
                    --data_name esconv \
                    --knowledge_name sbert \
                    --add_nlg_eval \
                    --add_mi_analysis \
                    --seed 13 \
                    --load_checkpoint ./DATA/strat.strat.esconv.sbert/2023-11-22142658.3e-05.16.1gpu/epoch-1.bin \
                    --fp16 false \
                    --max_input_length 256 \
                    --max_decoder_input_length 40 \
                    --max_length 40 \
                    --min_length 15 \
                    --infer_batch_size 64 \
                    --infer_input_file ./_reformat/ \
                    --temperature $temperature \
                    --top_k $top_k \
                    --top_p $top_p \
                    --num_beams $num_beams \
                    --repetition_penalty 1 \
                    --no_repeat_ngram_size 3
            done
        done
    done
done

#--load_checkpoint ./DATA/strat.strat.esconv.sbert/2023-10-25022042.3e-05.16.1gpu/epoch-2.bin \
#./DATA/strat.strat.esconv.sbert/2023-11-22002540.3e-05.64.1gpu/epoch-3.bin \
