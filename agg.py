#!/usr/bin/env python3

import sys
import statistics

def main():
    if len(sys.argv) == 1:
        print('need a file')
        sys.exit(1)

    scores = []
    for l in open(sys.argv[1]):
        if l.count('|') == 3 and l.count('.') > 0 and l[0] == '|':
            l = l.strip()
            parts = l.split('|')
            score = parts[2].strip()
            scores.append(float(score))

    print('n', len(scores))
    print('min', min(scores))
    print('max', max(scores))
    print('mean', statistics.mean(scores))

if __name__ == "__main__":
    main()
