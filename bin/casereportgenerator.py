#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:47:11 2021

@author: madeline
"""

'''
This script converts GVF to a TSV, for conversion to an HTML case report.
'''


import argparse
import pandas as pd
import os
import re



def parse_args():
    parser = argparse.ArgumentParser(
        description='Converts a GVF file to a TSV')
    parser.add_argument('--gvf', type=str, default=None,
                        help='Path to a GVF file')
    parser.add_argument('--outtsv', type=str, default='./case_report_tsvs/',
                        help='Output filepath for finished .tsv')
    return parser.parse_args()


def gvf2tsv(gvf):
    #read in gvf
    gvf_columns = ['#seqid','#source','#type','#start','#end','#score','#strand','#phase','#attributes']

    df = pd.read_csv(gvf, sep='\t', names=gvf_columns)    
    df = df[~df['#seqid'].str.contains("#")] #remove pragmas and original header
    df = df.reset_index(drop=True) #restart index from 0

    #split #attributes column into separate columns for each tag
    attributes = df['#attributes'].str.split(pat=';').apply(pd.Series) #split at ;, form dataframe
    attributes = attributes.drop(labels=len(attributes.columns)-1, axis=1) #last column is a copy of the index so drop it
    
    for column in attributes.columns:
        split = attributes[column].str.split(pat='=').apply(pd.Series)
        title = split[0].drop_duplicates().tolist()[0].lower()
        content = split[1]
        attributes[column] = content #ignore "tag=" in column content
        attributes.rename(columns={column:title}, inplace=True) #make attribute tag as column label

    #replace attributes column in the original df with the new separated out attributes
    df = pd.concat((df, attributes), axis=1)
    df = df.drop(labels='#attributes', axis=1)
    
    #remove '#' from column names
    df.columns = df.columns.str.replace("#", "")
    
    #drop unwanted columns
    df = df.drop(labels=['source', 'strand', 'score', 'phase', 'id'], axis=1)

    return df


if __name__ == '__main__':
    
    args = parse_args()
    
    filepath = args.outtsv
    gvf = args.gvf

    tsv_df = gvf2tsv(gvf)
    tsv_df.to_csv(filepath, sep='\t', index=False)
    
    print("Saved as: " + filepath)