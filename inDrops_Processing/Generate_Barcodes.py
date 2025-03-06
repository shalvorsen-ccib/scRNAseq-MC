# Code mostly adapted from Adrian Veres and indrops.py: https://github.com/indrops/indrops

import argparse
from itertools import product, combinations
import string


___tbl = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N'}
def rev_comp(seq):
    return ''.join(___tbl[s] for s in seq[::-1])



def main(bc_file, outfile):
    with open(bc_file, 'r') as f:
        bc2s = [line.rstrip() for line in f]
        rev_bc2s = [rev_comp(bc2) for bc2 in bc2s]
    barcode_iter = product(bc2s, rev_bc2s)
    with open(outfile, 'w') as out:
        for barcode in barcode_iter: 
            out.write(''.join(barcode) + '\n')
    return




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bc_file', default="gel_barcode2_list.txt", help='The file from indrops that contains barcodes. It is named gel_barcode2_list.txt')
    parser.add_argument('outfile', help="output file containing all possible bc combinations.")
    x = parser.parse_args()
    
    
    main(x.bc_file, x.outfile)