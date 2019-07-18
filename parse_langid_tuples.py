# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 13:43:00 2018

This script separates fastText language identification tuples into separate
columns and filters results. Outputs pickled dataframes of english and finnish
language texts.

Results are first filtered based on minimum probability, and minimum count of characters.

run this script with command:
    python parse_langid_tuples.py -i input.pkl -p fastText -o output.pkl

# NOTES: I used as input:
- P:\h510\some\data\finland\social_media\instagram\processed\Helsinki\instagram_hma_fasttext_langid.pkl

@author: Tuomas V., modified by Vuokko H.
"""

import pandas as pd
import argparse
import numpy as np

# Set up the argument parser
ap = argparse.ArgumentParser()

# Define arguments
ap.add_argument("-i", "--input", required=True,
                help="Path to the DataFrame containing userids.")
ap.add_argument("-p", "--preds", required=True,
                help="Name of the column containing language prediction tuple."
                "Order inside tuple must be: languages, probabilitys, lengths")
ap.add_argument("-o", "--output", required=True,
                help="Name of output pickled dataframe. This will receive a"
                " prefix of eng_ or fin_")

# Minimum accepted probability:
minprob = 0.5

#Minimum count of characters (based on number of characters per sentence fed to fasttext):
mincnt = 7

# Parse arguments
args = vars(ap.parse_args())

# Reading the preds with string lengths in
print('[INFO] - Reading in file...', args['input'])
preds = pd.read_pickle(args['input'])
print("len, original data:",len(preds))

# Drop unnecessary columns
print('[INFO] - Dropping rows without language info...')
preds = preds.loc[preds[args['preds']].isnull() == False]
print(preds[args['preds']].head())
print("len after dropping rows without language info:",len(preds))

print('[INFO] - Tresholding...')

# Apply the filtering function on each row of the dataframe
preds['langs'] = preds[args['preds']].apply(lambda x: list(np.array(x[0])[(np.array(x[1]) > minprob) & (np.array(x[2]) > mincnt)]) if x is not None else None)

# Apply the filtering function on each row of the dataframe
preds['probs'] = preds[args['preds']].apply(lambda x: list(np.array(x[1])[(np.array(x[1]) > minprob) & (np.array(x[2]) > mincnt)]) if x is not None else None)

# Check that everything looks ok..
print(preds[['langs', 'probs', args['preds']]].head(20))

# Setting the languages to remove duplicate identifications
print('[INFO] - Summarizing language info...')
preds['langs'] = preds['langs'].apply(lambda x: set(x) if x is not None else None)

# Extract english language posts and filter
print('[INFO] - Extracting english language posts...')
en_preds = preds.loc[preds['langs'] == {'en'}]
print("len of english posts:", len(en_preds))

# Extract finnish language posts and filter
fi_preds = preds.loc[preds['langs'] == {'fi'}]
print("len of Finnish posts:", len(fi_preds))

print('[INFO] - Writing results to file...')

# Saving the results
fi_preds.to_pickle('fin_' + args['output'])
en_preds.to_pickle('eng_' + args['output'])
preds.to_pickle(args['output'])