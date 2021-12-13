import argparse
import os
from tqdm import tqdm
import json
from spacy.lang.en import English

def main(av):
    
    data_path = av.data
    files = sorted(os.listdir(data_path))

    # Create a Tokenizer with the default settings for English including punctuation rules and exceptions
    tokenizer = English().tokenizer
    
    posting_list = dict()
    dgap_encoded_posting = dict()
    file2docid = dict()
    dgap_counts = {i:0 for i in range(len(files))}

    print("scanning corpus and building index .....")

    for i, file in enumerate(tqdm(files)):
        file2docid[i] = file
        content = open(os.path.join(data_path, file)).read()
        tokens = tokenizer(content) # get unique tokens from the document
        unique_tokens = set()
        for token in tokens:
            tok = token.text.lower()
            if tok.isalnum():
                if tok in unique_tokens:
                    continue
                unique_tokens.add(tok)
                posting_list.setdefault(tok, []).append(i)
                if len(posting_list[tok]) == 1:
                    dgap_counts[i] += 1
                    dgap_encoded_posting[tok] = [i]
                else:
                    gap = posting_list[tok][-1] - posting_list[tok][-2]
                    dgap_counts[gap] += 1
                    dgap_encoded_posting[tok].append(gap)

    res_path = '../result/part1.txt'
    open(res_path, 'w').write("\n".join(map(str, dgap_counts.values())))
    print(f'dgap counts written to {os.path.abspath(res_path)} .....')

    if av.cache:
        print('caching indexing results .....')
        json.dump((dgap_encoded_posting, dgap_counts), open('../indexing/cache.json', 'w'))
        print(f'encodings  and counts cached to cache.json')

    return dgap_encoded_posting, dgap_counts

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="/path/to/corpus/")
    ap.add_argument("--cache", action='store_true', help="inclusion of this flag indicates that indexing result should be cached")
    av = ap.parse_args()
    print(av)
    main(av)