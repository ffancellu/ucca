"""Feature extractor for UCCA scene-evoking classifier.

There are two kinds of features: lexical features extracted from the the
classified target word, and context features extracted from its instances
in non-UCCA corpora. In addition, extracting the class for the word from
UCCA passages is also covered.

"""

import argparse
import sys

from itertools import islice


DEFAULT_CHUNK_SIZE = 2 ** 20


def chunks(f, size=DEFAULT_CHUNK_SIZE):
    """Yields chunks of lines from a file until exhausted.

    Args:
        f: file to yield lines from
        size: hint to readlines() of how many bytes each yield should contain.

    Yields:
        list of strings (lines).

    """
    while True:
        x = f.readlines(size)
        if x:
            yield x
        else:
            raise StopIteration


def tokenize(sentences):
    """list of string sentences ==> list of tuples of stripped tokens"""
    return [tuple(x.strip().split()) for x in sentences if x.strip()]


def extract_ngrams(size, sentences, given=None):
    """Extracts all ngrams of the given size from the sentences.

    Args:
        size: the N parameter of the ngrams to extract
        sentences: sequence (can be generator) of tuples of strings, each
            is a token.
        given: previous ngram dictionary to start with. None otherwise.
            This dictionary isn't changed by the method.

    Returns:
        a new dictionary with (ngram, count) pairs.

    """

    if given is not None:
        counts = given.copy()
    else:
        counts = {}
    for s in sentences:
        if len(s) < size:
            continue
        for i in range((len(s) - size + 1)):
            counts[s[i:i + size]] = counts.get(s[i:i + size], 0) + 1
    return counts


def print_progress(current, updated=[0]):
    """Prints progress to stderr by adding current to updated[0] each time."""
    updated[0] = updated[0] + current
    print("Processed: " + str(updated[0]), file=sys.stderr)


def parse_cmd():
    """Parses and validates cmd line arguments, then return them."""
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('ngrams',))
    parser.add_argument('action', choices=('extract',))
    parser.add_argument('--ngram_size', type=int, default=1)
    parser.add_argument('--sort', action='store_true')

    args = parser.parse_args()
    return args


def main():
    args = parse_cmd()
    if args.command == 'ngrams' and args.action == 'extract':
        counts = None
        for data in chunks(sys.stdin):
            sentences = tokenize(data)
            counts = extract_ngrams(args.ngram_size, sentences, counts)
            print_progress(len(sentences))
        print("Finished processing", file=sys.stderr)
        if args.sort:
            sorted_counts = sorted(counts.items(), key=lambda x: x[1],
                                   reverse=True)
            print('\n'.join('\t'.join([str(value), ' '.join(ngram)])
                        for ngram, value in sorted_counts))
        else:
            for ngram, value in counts.items():
                print('\t'.join([str(value), ' '.join(ngram)]))


if __name__ == '__main__':
    main()