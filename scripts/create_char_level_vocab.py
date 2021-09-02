#!/usr/bin/env python3

import sys


def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        for line in f:
            item, freq = line.strip().split()
            if not freq.startswith('-'):
                print(f'{item}\t{freq}')
            elif len(item) == 1:
                print(f'{item}\t{freq}')

if __name__ == '__main__':
    main()
