# Index Compression

This contains code to compress dgap posting lists in an inverted index of a corpus using methods like Elias-Gamma encoding, Golomb encoding, and Arithmetic encoding.

```plaintext
usage: compression.py [-h] --data DATA [--cache]

optional arguments:
  -h, --help   show this help message and exit
  --data DATA  /path/to/corpus/
  --cache      argument to indicate caching of data received from indexing (if previous cache doesn't exist)
```

Example:

```bash
python compression.py --data [path/to/data/directory]
```

Choice of hyperparameters: 
* ***m*** in Golomb encoding is set to be **15** as it gave the best compression of posting list among the given constraint that $m \in [1,15]$

Author: [Shubham Lohiya](https://shubhlohiya.github.io/)