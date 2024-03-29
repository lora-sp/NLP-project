import preprocessing as pp
import json
import random

eval_files = []
for filename in pp.filenames:
    random.seed(3)
    eval = random.sample((pp.csv_to_paragraphs(filename)), 2) # 2 paragraphs selected randomly from each manifesto
    eval_files.append(eval)
    with open("evaluation/eval_" + filename[:-14] + ".json", 'w', encoding='utf-8') as f:
        json.dump(eval, f, ensure_ascii=False, indent=3)

