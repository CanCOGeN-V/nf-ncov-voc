#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: zohaib

This script uses assets/ncov_variants_who_variants.tsv as key and
lists the lineages corresponding to VOCs, VOIs and VUMs in input
dataset for extracting metadata.

"""

import argparse
import pandas as pd
import csv


def parse_args():
    parser = argparse.ArgumentParser(
        description='List of Variants of Concern and Interest from')
    parser.add_argument('--variants', type=str, default=None,
                        help='WHO variants OR custom variants')
    parser.add_argument('--metadata', type=str, default=None,
                        help='metadata file')
    parser.add_argument('--outfile', type=str, default=None,
                        help='list of lineages in output file')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    who_lineages = []
    variants = pd.read_csv(args.variants, sep="\t",
                           low_memory=False)

    for var in variants["pango_lineage"]:
        #print(var)
        if "," in var:
            #temp = var.split(",")
            for temp in var.split(","):
                if not "[" in var:
                    who_lineages.append(temp)
                else:
                    parent=temp[0]
                    child=temp[2:-3].split("|")
                    for c in child:
                        who_lineages.append(parent + str(c))
                        who_lineages.append(parent+str(c)+".*")
        else:
            who_lineages.append(var)


    Metadata = pd.read_csv(args.metadata, sep="\t", low_memory=False)
    lineages = Metadata['lineage'].unique()

    parsed_lineages=[]
    for lineage in lineages:
        for who_lin in who_lineages:
            if "*" in who_lin:
                who_lin = who_lin[:-1]
                if isinstance(lineage, str) and lineage.startswith(
                        who_lin):
                    parsed_lineages.append(lineage)
            else:
                if lineage == who_lin:
                    parsed_lineages.append(lineage)

    with open(args.outfile, 'w') as f:
        for item in sorted(set(parsed_lineages)):
            f.write("%s\n" % item)
