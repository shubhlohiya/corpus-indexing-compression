import argparse
import os
import sys
import json
sys.path.append("..")
from indexing.indexing import main as get_index
from utils import gamma_encoding, golomb_encoding, arithmetic_encoding, get_dgap_cumulative_dist

def main(av):
    
    try:
        dgap_encoded_posting, dgap_counts = json.load(open('../indexing/cache.json'))
        print('loaded index from cache')
    except:
        print('cache not found, rebuilding index .....')
        dgap_encoded_posting, dgap_counts = get_index(av)

    print('compressing index using gamma and golomb encoding .....')

    gamma_enc_lookup = {i: gamma_encoding(i) for i in range(len(dgap_encoded_posting))}
    golomb_enc_lookup = {i: golomb_encoding(i, m=15) for i in range(len(dgap_encoded_posting))}
    # m = 15 gave best golomb compression among given constrained interval [1,15]

    gamma_enc_posting = {tok: "".join([gamma_enc_lookup[n] for n in list_]) for tok, list_ in dgap_encoded_posting.items()}
    golomb_enc_posting = {tok: "".join([golomb_enc_lookup[n] for n in list_]) for tok, list_ in dgap_encoded_posting.items()}

    sorted_tokens = sorted(dgap_encoded_posting.keys())
    original_sizes = " ".join([str(32*len(dgap_encoded_posting[token])) for token in sorted_tokens])
    gamma_sizes = " ".join([str(len(gamma_enc_posting[token])) for token in sorted_tokens])
    golomb_sizes = " ".join([str(len(golomb_enc_posting[token])) for token in sorted_tokens])

    res_path = '../result/part2.txt'
    open(res_path, 'w').write("\n".join([original_sizes, gamma_sizes, golomb_sizes]))
    print(f'compressed size info of various compression algorithms written to {os.path.abspath(res_path)}')

    print('calculating arithmetic encoding for various dgaps .....')

    cdf = get_dgap_cumulative_dist(dgap_counts)
    res_path = '../result/arith.txt'
    open(res_path, 'w').write("\n".join(f'{gap} {arithmetic_encoding(gap, cdf)}' for gap in dgap_counts))
    print(f'arithmetic encodings of all possible dgaps written to {os.path.abspath(res_path)}')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="/path/to/corpus/")
    ap.add_argument("--cache", action='store_true', help='argument for caching data received from indexing')
    av = ap.parse_args()
    main(av)