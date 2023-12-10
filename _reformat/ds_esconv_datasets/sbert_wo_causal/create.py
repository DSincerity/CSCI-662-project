import json
import glob

file_paths = glob.glob("*.txt")

def get_causal(input_str):
    return input_str.replace(input_str[input_str.find("[str]"):input_str.find("[aff]")], "")

def get_xintent(input_str):
    return input_str.replace(input_str[input_str.find("[xIntent]"):input_str.find("[xWant]")], "")

for file_path in file_paths:
    with open(file_path, "r") as f:
        lines = f.readlines()
        data = [json.loads(i) for i in lines]
    
    for dialog in data:
        for utterance in dialog["dialog"]:
            if "heal" in utterance.keys() and utterance["heal"] != "":
                utterance["heal"] = str(get_causal(utterance["heal"]))
            elif "knowledge" in utterance.keys() and utterance["knowledge"] != "":
                utterance["knowledge"] = str(get_xintent(utterance["knowledge"]))

    with open(f"{file_path}", "w+") as f:
        for dialog in data:
            f.write(json.dumps(dialog) + "\n")
