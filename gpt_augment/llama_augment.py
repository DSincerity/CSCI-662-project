import json
from transformers import AutoTokenizer
import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import logging
logging.basicConfig(level='ERROR')


def generate(file_path, model_name, output_file, device):
    with open(file_path, "r") as f:
        lines = f.readlines()
        data = [json.loads(i) for i in lines]

    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def mapper_heal(x):
        messages=[
                {
                "role": "user",
                "content": "Generate a potential response, stressor and affective status for the following dialogue utterance. For example:\n\nUtterance: Losing a job is always anxious.\nAssistant: [resp] could you get a job? [str] extremy, whenevrt, teachers, ground, havent [aff] Afraid\n\nUtterance: {text}\nAssistant: "
                }
            ]
        messages[0]["content"] = messages[0]["content"].format(text=x)
        return tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)

    def mapper_comet(x):
        messages=[
                {
                "role": "user",
                "content": "Generate a potential reaction, intent, want, need and effect for the following dialogue utterance. For example:\n\nUtterance: I'm feeling anxious that I am going to lose my job.\nAssistant: [xReact] worried [xIntent] none [xWant] to get a new job [xNeed] none [xEffect] frowns\nUtterance: {text}\nAssistant: "
                }
            ]
        messages[0]["content"] = messages[0]["content"].format(text=x)
        return tokenizer.apply_chat_template(messages, return_tensors="pt").to(device)


    def generate_comet_knowledge(text):
        text = mapper_comet(text)
        generated_ids = model.generate(text, max_new_tokens=64, do_sample=True, temperature=0.1, top_k=10, top_p=0.9)
        decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return decoded[0]


    def generate_heal_knowledge(text):
        text = mapper_heal(text)
        generated_ids = model.generate(text, max_new_tokens=64, do_sample=True, temperature=0.1, top_k=10, top_p=0.9)
        decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return decoded[0]


    with open(output_file, "w+") as f:
        for index, dialogue in enumerate(tqdm(data)):
            for index_utter, utterance in enumerate(tqdm(dialogue["dialog"])):
                if utterance["speaker"] == "usr":
                    utterance["knowledge"] = generate_comet_knowledge(utterance["text"])
                elif utterance["speaker"] == "sys":
                    utterance["knowledge"] = generate_heal_knowledge(utterance["text"])
            f.write(json.dumps(dialogue) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str, required=False, default="../_reformat/esconv/sbert/train.txt")
    parser.add_argument("--model_name", type=str, required=False, default="mistralai/Mistral-7B-Instruct-v0.1")
    parser.add_argument("--output_file", type=str, required=False, default="mistral_train.txt")
    parser.add_argument("--device", type=str, required=False, default="cuda")
    args = parser.parse_args()
    
    generate(args.file_path, args.model_name, args.output_file, args.device)
