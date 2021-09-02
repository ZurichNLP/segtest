#!/usr/bin/env python3

import sys
from collections import OrderedDict

import json


def main():
    for filename in sys.argv[1:]:
        print('Processing', filename)
        sorted_words = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words_in = line.strip().split()
                sorted_words.append(words_in[0])

        worddict = OrderedDict()
        worddict['<EOS>'] = 0
        worddict['<GO>'] = 1
        worddict['<UNK>'] = 2
        for ii, ww in enumerate(sorted_words[3:]):
            worddict[ww] = ii+3
            
        with open('%s.json'%filename, 'w', encoding='utf-8') as f:
            json.dump(worddict, f, indent=2, ensure_ascii=False)

        print('Done')

if __name__ == '__main__':
    main()
