#!/usr/bin/env python
u"""
make_grace_index.py
Written by Tyler Sutterley (08/2022)
Creates index files of GRACE/GRACE-FO Level-2 data

CALLING SEQUENCE:
    python make_grace_index.py --version 0 1

COMMAND LINE OPTIONS:
    --help: list the command line options
    -D X, --directory X: working data directory
    -c X, --center X: GRACE/GRACE-FO Processing Center
    -r X, --release X: GRACE/GRACE-FO Data Releases to run
    -v X, --version X: GRACE/GRACE-FO Level-2 Data Version to run
    -M X, --mode X: Local permissions mode of the files created

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html

UPDATE HISTORY:
    Written 08/2022
"""
from __future__ import print_function

import sys
import os
import logging
import argparse
from gravity_toolkit.utilities import compile_regex_pattern

#-- PURPOSE: Creates index files of GRACE/GRACE-FO data
def make_grace_index(DIRECTORY, PROC=[], DREL=[], VERSION=[], MODE=None):

    #-- mission shortnames
    shortname = {'grace':'GRAC', 'grace-fo':'GRFO'}
    #-- datasets for each processing center
    DSET = {}
    DSET['CSR'] = ['GAC', 'GAD', 'GSM']
    DSET['GFZ'] = ['GAA', 'GAB', 'GAC', 'GAD', 'GSM']
    DSET['JPL'] = ['GAA', 'GAB', 'GAC', 'GAD', 'GSM']

    #-- GRACE/GRACE-FO level-2 spherical harmonic products
    logging.info('GRACE/GRACE-FO L2 Global Spherical Harmonics:')
    #-- for each processing center (CSR, GFZ, JPL)
    for pr in PROC:
        #-- for each data release (RL04, RL05, RL06)
        for rl in DREL:
            #-- for each level-2 product (GAC, GAD, GSM, GAA, GAB)
            for ds in DSET[pr]:
                #-- local directory for exact data product
                local_dir = os.path.join(DIRECTORY, pr, rl, ds)
                #-- list of GRACE/GRACE-FO files for index
                grace_files = []
                #-- for each satellite mission (grace, grace-fo)
                for i,mi in enumerate(['grace','grace-fo']):
                    #-- print string of exact data product
                    logging.info('{0} {1}/{2}/{3}'.format(mi, pr, rl, ds))
                    #-- regular expression operator for data product
                    rx = compile_regex_pattern(pr, rl, ds,
                        mission=shortname[mi], version=VERSION[i])
                    #-- find local GRACE/GRACE-FO files to create index
                    files = [fi for fi in os.listdir(local_dir) if rx.match(fi)]
                    #-- extend list of GRACE/GRACE-FO files
                    grace_files.extend(files)

                #-- outputting GRACE/GRACE-FO filenames to index
                with open(os.path.join(local_dir,'index.txt'),'w') as fid:
                    for fi in sorted(grace_files):
                        print('{0}'.format(fi), file=fid)
                #-- change permissions of index file
                os.chmod(os.path.join(local_dir,'index.txt'), MODE)

#-- PURPOSE: create argument parser
def arguments():
    parser = argparse.ArgumentParser(
        description="""Creates index files of GRACE/GRACE-FO
            monthly Level-2 data
            """
    )
    #-- command line parameters
    # #-- working data directory
    parser.add_argument('--directory','-D',
        type=lambda p: os.path.abspath(os.path.expanduser(p)),
        default=os.getcwd(),
        help='Working data directory')
    #-- GRACE/GRACE-FO processing center
    parser.add_argument('--center','-c',
        metavar='PROC', type=str, nargs='+',
        default=['CSR','GFZ','JPL'], choices=['CSR','GFZ','JPL'],
        help='GRACE/GRACE-FO processing center')
    #-- GRACE/GRACE-FO data release
    parser.add_argument('--release','-r',
        metavar='DREL', type=str, nargs='+',
        default=['RL06'], choices=['RL06'],
        help='GRACE/GRACE-FO data release')
    #-- GRACE/GRACE-FO data version
    parser.add_argument('--version','-v',
        metavar='VERSION', type=str, nargs=2,
        default=['0','1'], choices=['0','1','2','3'],
        help='GRACE/GRACE-FO Level-2 data version')
    #-- permissions mode of the directories and files synced (number in octal)
    parser.add_argument('--mode','-M',
        type=lambda x: int(x,base=8), default=0o775,
        help='Permission mode of files created')
    #-- return the parser
    return parser

#-- This is the main part of the program that calls the individual functions
def main():
    #-- Read the system arguments listed after the program
    parser = arguments()
    args,_ = parser.parse_known_args()

    #-- run program with parameters
    make_grace_index(args.directory, PROC=args.center,
        DREL=args.release, VERSION=args.version,
        MODE=args.mode)

#-- run main program
if __name__ == '__main__':
    main()