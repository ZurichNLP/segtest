#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import argparse

from typing import List, Dict, Tuple

import string
from collections import defaultdict

TRANSLATOR = str.maketrans('', '', string.punctuation + '“' + '”' + "'")
ALL_VOWELS = "AaEeIiOoUuÄäÜüÖö"

# Order according to pattern pair frequency: surface forms
COMPOUND_SURFACE_ORDER = ['sona_surface-bico', 'zogaze_surface-qepus', 'suyi_surface-saqo', 'segalo_surface-domabu', 'zarumo_surface-vazaga', 'tumoko_surface-pifeke', 'necib_surface-kixaka', 'yoyexo_surface-nifa', 'dawida_surface-nonujo', 'saxuj_surface-tedubo']
VOWEL_HARMONY_SURFACE_ORDER = ["duji_surface-['s', 'f', 'p']", "zoged_surface-['b', 'p', 'r']", "dulana_surface-['n', 'l', 'j']", "xefoqi_surface-['b', 'k', 'm']"]
INFIX_SURFACE_ORDER = ['jetah_surface-huheke', 'dezaxe_surface-siye', 'yusid_surface-huxi', 'yadey_surface-numime']
CIRCUMFIX_SURFACE_ORDER = ["['jeb', 'fet']_surface-wofi", "['Kur', 'maz']_surface-quroc", "['nuw', 'daf']_surface-seyet", "['Rül', 'bos']_surface-sudizu"]
REDUPLICATION_SURFACE_ORDER = ['partial_surface-popera', 'triple_partial_surface-metuza', 'full_surface-gija']

# Order according to pattern pair frequency: abstract forms
COMPOUND_ABSTRACT_ORDER = ['@COMPOUND_1@_abstract-wuze', '@COMPOUND_2@_abstract-pomuy', '@COMPOUND_3@_abstract-quyeso', '@COMPOUND_4@_abstract-zolo', '@COMPOUND_5@_abstract-nemine', '@COMPOUND_6@_abstract-fexot', '@COMPOUND_7@_abstract-zixu', '@COMPOUND_8@_abstract-tazif', '@COMPOUND_9@_abstract-supu', '@COMPOUND_10@_abstract-jifo']
VOWEL_HARMONY_ABSTRACT_ORDER = ['raxuja_abstract-@VOWEL_HARMONY_1@', 'gapu_abstract-@VOWEL_HARMONY_2@', 'soyut_abstract-@VOWEL_HARMONY_3@', 'zide_abstract-@VOWEL_HARMONY_4@']
INFIX_ABSTRACT_ORDER = ['@INFIX_1@_abstract-soxu', '@INFIX_2@_abstract-ceri', '@INFIX_3@_abstract-lasi', '@INFIX_4@_abstract-jigaq']
CIRCUMFIX_ABSTRACT_ORDER = ['@CIRCUMFIX_1@_abstract-fuge', '@CIRCUMFIX_2@_abstract-zixer', '@CIRCUMFIX_3@_abstract-xobex', '@CIRCUMFIX_4@_abstract-pasoz']
REDUPLICATION_ABSTRACT_ORDER = ['partial_abstract-gegec', 'triple_partial_abstract-yisu', 'full_abstract-jufo']

ORDER_LOOKUP = {'surface': {'infix': INFIX_SURFACE_ORDER,
                            'circumfix': CIRCUMFIX_SURFACE_ORDER,
                            'vowelharmony': VOWEL_HARMONY_SURFACE_ORDER,
                            'compound': COMPOUND_SURFACE_ORDER,
                            'reduplication': REDUPLICATION_SURFACE_ORDER},
                'abstract': {'infix': INFIX_ABSTRACT_ORDER,
                             'circumfix': CIRCUMFIX_ABSTRACT_ORDER,
                             'vowelharmony': VOWEL_HARMONY_ABSTRACT_ORDER,
                             'compound': COMPOUND_ABSTRACT_ORDER,
                             'reduplication': REDUPLICATION_ABSTRACT_ORDER}}

FREQS = ['zero-shot', '1-5', '6-15', '16-50', '51-100', '101-500', '501-1000']


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser('evaluate.py',
                                     description='''Evaluation for translation
                                     of morphological phenomena.''')
    parser.add_argument('-t', '--translations',
                        help='Output of machine translation model.',
                        type=argparse.FileType(encoding='utf-8'),
                        required=True)
    parser.add_argument('-i', '--meta_info',
                        help='''Meta info file: stores the patterns that should
                        occur in the MT output and how frequent they are
                        in the training data.''',
                        type=argparse.FileType(encoding='utf-8'),
                        required=True)
    parser.add_argument('-s', '--scores',
                        help='''Language model scores for augmented data
                        (-inf for original sentences).''',
                        type=argparse.FileType(encoding='utf-8'),
                        required=True)
    parser.add_argument('-m', '--morphological_phenomenon',
                        help='Morphological phenomenon that is evaluated.',
                        type=str,
                        choices=['circumfix', 'compound', 'infix',
                                 'reduplication', 'vowelharmony'],
                        required=True)
    parser.add_argument('-r', '--representation_type',
                        help='''Representation that is used
                        for morphological phenomena.''',
                        type=str,
                        choices=['surface', 'abstract'],
                        required=True)
    parser.add_argument('--include_augmented_examples',
                        help='''Compute accuracy on original test examples
                        and examples generated with data augmentation).''',
                        action='store_true')
    parser.add_argument('--evaluate_by_freq_buckets',
                        help='''Compute accuracy within source frequency
                        buckets instead of over all examples.''',
                        action='store_true')
    return parser


def get_order(morphological_phenomenon: str,
              representation_type: str) -> List[str]:
    """Returns a specific order of pattern pairs."""
    return ORDER_LOOKUP[representation_type][morphological_phenomenon]


def get_freq_band(freq: int) -> str:
    """Returns the corresponding source frequency bucket. We do not consider
    examples where the word is seen more than 1000 times in the training data
    with this morphological phenomenon."""
    if freq == 0:
        return 'zero-shot'
    elif freq > 0 and freq <= 5:
        return '1-5'
    elif freq > 5 and freq <= 15:
        return '6-15'
    elif freq > 15 and freq <= 50:
        return '16-50'
    elif freq > 50 and freq <= 100:
        return '51-100'
    elif freq > 100 and freq <= 500:
        return '101-500'
    elif freq > 500 and freq <= 1000:
        return '501-1000'


def get_string_without_punct(token: str) -> str:
    """Removes all type of punctuation from a string."""
    # apostrophe in possessives and internal hyphens should not be deleted
    punct_to_ignore = ["'", '-']
    for num, punct in enumerate(punct_to_ignore):
        if punct in token and not token.endswith(punct):
            token = re.sub('-', f'@@@{num}', token)
    token = token.translate(TRANSLATOR)
    for num, punct in enumerate(punct_to_ignore):
        if punct in token and not token.endswith(punct):
            token = re.sub(f'@@@{num}', '-', token)
    return token


def extract_info(pattern: str) -> Tuple[str, str, str, str]:
    """Extracts all information needed to evaluate an example."""
    pattern = pattern.strip().split('\t')
    pattern_pair = pattern[0]
    annotations, to_match = pattern[1].split(':')
    side, src_freq, _ = annotations.split('-')
    freq_band = get_freq_band(int(src_freq))
    return pattern_pair, to_match, side, freq_band


def found_single_token(to_match: str, translation: str) -> bool:
    """Checks for a specific single tokens in a string."""
    matches = re.findall(r'\s?'+to_match+r'\S*?\s', translation)
    return len(matches) == 1


def found_reduplication(to_match: str, translation: str) -> bool:
    """Checks for a reduplicated token in a string."""
    # first check if the reduplication from the reference translation occurs
    matches = re.findall(r'\s?'+to_match+r'\S*?\s', translation)
    results = len(matches) == 1
    # otherwise check if there is another reduplicated token in the translation
    if not results:
        matches = re.findall(r'\s?(\S\S\S+)\1\S*?\s', translation)
        results = len(matches) == 1
    return results


def found_infix(to_match: str, translation: str) -> bool:
    """Checks for an infixed token in a string."""
    # find a token that contains the correct fake morpheme
    matches = re.findall(r'\s?(\S+)?'+to_match+r'(\S*)?\s', translation)
    return len(matches) == 1


def found_circumfix(to_match: str, translation: str) -> bool:
    """Checks for a circumfixed token in a string."""
    # find a token that starts with the correct fake morpheme and ends with
    # the correct fake morpheme
    part1, part2 = to_match.split('-')
    matches = re.findall(r'\s?'+part1+r'(\S+)?'+part2+r'\S*?\s', translation)
    return len(matches) == 1


def found_vowel_harmony(to_match: str,
                        translation: str,
                        toks: List[str],
                        orig_toks: List[str]) -> bool:
    """Checks for a correct vowel harmony in a string."""
    # get consonant triple from token to match
    consonants = re.findall(r"[^"+ALL_VOWELS+r"]+", to_match)
    beginning = consonants[0]
    middle = consonants[1]
    end = consonants[2]
    # find a token that has these consonants in the translation
    pattern = beginning+r'['+ALL_VOWELS+r']+'+middle+r'['+ALL_VOWELS+r']+'+end
    results = re.findall(pattern, translation)
    if results:
        vowels = re.findall(r"["+ALL_VOWELS+r"]+", results[0])
        try:
            # find vowels in preceeding token
            pattern_index = toks.index(results[0])
            prev_word = orig_toks[pattern_index - 1]
            prev_vowels = re.findall("["+ALL_VOWELS+"]+", prev_word)
            # check if the last two vowels of the preceeding token agree with
            # the vowel harmony token
            if len(prev_vowels) > 1:
                return (vowels[0].lower() == prev_vowels[-2].lower()) \
                        and (vowels[1].lower() == prev_vowels[-1].lower())
            # for preceeding tokens with only one vowel, the same vowel appears
            # twice in the vowel harmony token
            elif len(prev_vowels) == 1:
                return (vowels[0].lower() == prev_vowels[-1].lower()) \
                        and (vowels[1].lower() == prev_vowels[-1].lower())
        except ValueError:  # vowel harmony is not separate token
            return False
    return False


def evaluate(args: argparse.Namespace) -> Tuple[Dict, Dict]:
    """Evaluates morphological phenomena in a set of examples."""

    # setup counters to compute accuracy
    total = defaultdict(int)
    accurate = defaultdict(int)

    for pattern, translation, score in zip(args.meta_info,
                                           args.translations,
                                           args.scores):
            score = score.strip()
            # original (not augmented) examples have a score of -inf
            if args.include_augmented_examples or score == '-inf':
                # extract on which side the morphological pattern occurs,
                # which `fake' morpheme we need to match and
                # which source frequency bucket the example belongs in
                pattern_pair, to_match, side, freq_band = extract_info(pattern)

                # check if example uses surface or abstract representation
                representation_type = pattern_pair.split('-')[0].split('_')[-1]
                if representation_type == args.representation_type:

                    # for vowel harmony we need access to individual tokens
                    orig_toks = translation.strip().split(' ')
                    toks = [get_string_without_punct(t) for t in orig_toks]

                    # ignore examples in source frequency bucket > 1000 because
                    # for many pattern pairs we do not have enough examples in
                    # this category for a reliable evaluation
                    if freq_band:
                        # we evaluate on lower-cased data
                        to_match = to_match.lower()
                        translation = translation.lower()
                        results = False

                        # cases where we only need to match an isolated `fake'
                        # morpheme or an abstract token in the MT output
                        if args.morphological_phenomenon in ['compound'] \
                           or side == 'src' \
                           or representation_type == 'abstract':
                            results = found_single_token(to_match, translation)

                        # trg-side reduplication: we match if the reference
                        # pattern is found or if there is a reduplicated token
                        elif args.morphological_phenomenon == 'reduplication' \
                            and side == 'trg':
                            results = found_reduplication(to_match, translation)

                        # trg-side infixation: we match if the `fake' morpheme
                        # occurs inside a token
                        elif args.morphological_phenomenon == 'infix' \
                            and side == 'trg':
                            results = found_infix(to_match, translation)

                        # trg-side circumfixation: we match if there is a token
                        # with `fake' prefix and `fake' suffix
                        elif args.morphological_phenomenon == 'circumfix' \
                            and side == 'trg':
                            results = found_circumfix(to_match, translation)

                        # trg-side vowel harmony: we match if the correct
                        # consonant triple occurs in the output and then check
                        # if the vowels between match the last two vowels of
                        # the preceeding token
                        elif args.morphological_phenomenon == 'vowelharmony' \
                            and side == 'trg':
                            results = found_vowel_harmony(to_match,
                                                          translation,
                                                          toks,
                                                          orig_toks)

                        if args.evaluate_by_freq_buckets:
                            pattern_pair += '-' + freq_band

                        if results is True:
                            accurate[pattern_pair] += 1
                        total[pattern_pair] += 1

    return total, accurate


def print_results(num: int,
                  pattern: str,
                  accurate: Dict,
                  total: Dict,
                  freq: int=None) -> None:

    description = f'{num + 1} {freq}' if freq else f'{num + 1}'
    try:
        print(f'#{description}: {round(accurate[pattern] / total[pattern], 3)}')
    except ZeroDivisionError:
        print(f'#{description}: no examples found for this pattern')


def main() -> None:

    parser = create_argument_parser()
    args = parser.parse_args()

    # run evaluation for given phenomenon
    total, accurate = evaluate(args)

    ordered_pairs = get_order(args.morphological_phenomenon,
                              args.representation_type)

    # print results to command line, either by frequency or overall
    for pattern_num, pattern_pair in enumerate(ordered_pairs):
        if args.evaluate_by_freq_buckets:
            for freq in FREQS:
                pattern_key = pattern_pair+'-'+freq
                print_results(pattern_num, pattern_key, accurate, total, freq)
            print()
        else:
            print_results(pattern_num, pattern_pair, accurate, total)


if __name__ == '__main__':
    main()
