import json
import glob

file_paths = glob.glob("*.txt")

import re

def get_aff(input_str):
    match = re.search(r'\[aff\] (\w+)', input_str)
    if match:
        return input_str.replace("[aff] " + match.group(1), "")
    else:
        return None

def get_xreact(input_str):
    match = re.search(r'\[xReact\] (\w+)', input_str)
    if match:
        return input_str.replace("[xReact] " + match.group(1), "")
    else:
        return None

for file_path in file_paths:
    with open(file_path, "r") as f:
        lines = f.readlines()
        data = [json.loads(i) for i in lines]
    
    for dialog in data:
        for utterance in dialog["dialog"]:
            if "heal" in utterance.keys() and utterance["heal"] != "":
                utterance["heal"] = str(get_aff(utterance["heal"]))
            elif "knowledge" in utterance.keys() and utterance["knowledge"] != "":
                utterance["knowledge"] = str(get_xreact(utterance["knowledge"]))

    with open(f"{file_path}", "w+") as f:
        for dialog in data:
            f.write(json.dumps(dialog) + "\n")