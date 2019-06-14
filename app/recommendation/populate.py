import os, sys

import django
import pandas as pd
from models import Scotch

# Start execution here!
if __name__ == '__main__':

    print("Starting Scotch population script...")

    os.environ['DJANGO_SETTINGS_MODULE'] = 'scotchy_app.settings'
    
    ### Scotch dataframe
    scotch_db = pd.read_csv('../data/processed/scotch_db.csv', index_col=0)
    # populate Scotch table
    for s in d.itertuples():Scotch.objects.create(name=s.name, age=s.age)

    """
    clear teh SQLite table
    DELETE FROM your_table; DELETE FROM SQLite_sequence WHERE name='your_table';
    """

    ### emotion synonym json
    with open('../data/processed/emotion_ds.json') as f: 
		emotion_syn = json.load(f) 
	f.close() 

    
	for k,v in emotion_syn.items(): 
 		EmotionSyn.objects.create(parent_emotion=k, synonyms=v) 

 	### adjectives
	with open('../data/processed/adjs.json') as f: 
		adjs = json.load(f) 
	f.close() 

	for k,v in emotion_syn.items(): 
 		Summaries.objects.create(summary=v)