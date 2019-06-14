import random
import json
import pandas as pd
import numpy as np
import spacy

# paths to files
product_database = '../data/processed/scotch_df.csv'
product_emotion_sim = '../data/processed/similarity_emotion_scotch.npy'
summary_dictionary = '../data/processed/adjs.json'
emotion_synonyms = '../data/processed/emotion_ds.json'

class RecommendationEngine():
	"""
	This class uses affective AI to recommend a product from a database based on
	a user's emotional state. In its current version, it uses precomputed
	document similarity metrics and adjective lists to speed up processing time.

	Inputs:

	product_database - a database of product descriptions
	product_emotion_sim - a numpy matrix of precomputed document similarity scores between
						  emotional states and product descriptions
	summary_dictionary - a json file of adjectives pulled from product desriptions
	emotion_synonyms - a json file of parent emotions and their synonyms
	"""

	def __init__(self, product_database, product_emotion_sim, summary_dictionary, emotion_synonyms):

		# database of scotch metadata
		self.scotch_df = pd.read_csv(product_database, index_col=0)
		# similarity between scotch descriptions and emotions
		self.sim_emo_scotch = np.load(product_emotion_sim)
		# dictionary of scotch summaries
		with open(summary_dictionary, 'r') as f:
			self.summaries = json.load(f)
		f.close()
		# dictionary of emptions and synonyms
		with open(emotion_synonyms) as f:
			self.emotion_dict = json.load(f)
		f.close()
		# indices for emotion dictionary
		self.emotion_idx = {}
		# populate indices
		for i, k in enumerate(self.emotion_dict.keys()):
			self.emotion_idx[k] = i

	def scotch_scotch_sim(self, match_on, array):

		"""
		A method for calculating the document similarity using spacy between
		two product descriptions using word embeddings.

		Inputs:

		match_on - column name to match products on (e.g. descriptions)
		array - a numpy array to store similarity scores
		"""

		# initialize English model
		nlp = spacy.load('en_core_web_lg')

		# list of index values
		idx_vals = self.scotch_df.index.values

		# loop through entries
		for i in idx_vals:
			# store name
			scotch_id = i
			# create document
			doc_1 = nlp(self.scotch_df.loc[i, match_on])
			# initiate index vals to compare against
			idx_loop = [idx for idx in idx_vals if idx != i]
			# loop through
			for idx in idx_loop:
				# create document to match
				doc_2 = nlp(self.scotch_df.loc[idx, match_on])
				# populate dictionary
				array[scotch_id][idx] = doc_1.similarity(doc_2) 

	def emotion_scotch_sim(self, match_on, array):
		"""
		A method for calculating the document similarity using spacy between
		a product description and an emotions and its synonyms
		using word embeddings.

		Inputs:

		match_on - column name to match products on (e.g. descriptions)
		array - a numpy array to store similarity scores
		"""

		# initialize English model
		nlp = spacy.load('en_core_web_lg')

		# list of index values
		idx_vals = self.scotch_df.index.values

		# loop through entries
		for i in idx_vals:
			# store name
			scotch_id = i
			# create document
			doc_1 = nlp(self.scotch_df.loc[i, match_on])
			# loop through emotions
			for idx, e in self.emotion_idx.items():
				# create document to match by combining master emotion with synonyms
				doc_2 = nlp(e + ' ' + ' '.join(emotion_syn[v]))
				# populate dictionary
				array[idx][scotch_id] = doc_1.similarity(doc_2) 

	def match_emotion(self, emotion):
		"""
		A method for calculating the document similarity using spacy between
		a novel emotional state and the list of parent emotions.

		Inputs:

		emotion - a novel emotional state
		"""

		# dict to store similarity values
		similarity = {}

		for k,v in self.emotion_dict.items():
			# check and see if emotion matches one in dictionary
			if emotion == k or emotion in v:
				# if so, return emotion
				return k
			else:
				pass

		# if not, calculate similarity between emotion and dictionary
		for k,v in self.emotion_dict.items():
			# initialize English model
			nlp = spacy.load('en_core_web_lg')

			doc1 = nlp(emotion)
			doc2 = nlp(k)
			similarity[k] = doc1.similarity(doc2)

			# return max
			return max(similarity, key=similarity.get) 

	def get_rec(self, emotion):

		"""
		A method that randomly samples 3 products from the top 25 similarity
		matches between a product and an emotion.

		Inputs:

		emotion - a user's input emotional state
		"""

		# get the emotion for recommendation
		self.rec_emotion = self.match_emotion(emotion)
		# get index of emotion
		self.rec_idx = self.emotion_idx[self.rec_emotion]
		# get indices of top three scotches based on precomputed similarity scores
		scotch_idx = random.sample(list(self.sim_emo_scotch.argsort()[self.rec_idx][-25:][::-1]), 1)[0]
		# dictionary to hold recommendation data
		self.recs = {}
		# populate dictionary
		self.recs['Name'] = self.scotch_df.loc[scotch_idx, 'name']
		self.recs['Age'] = self.scotch_df.loc[scotch_idx, 'age']
		if len(self.summaries[str(scotch_idx)]) > 3:
			self.recs['Summary'] = random.sample(self.summaries[str(scotch_idx)], 3)
		else:
			self.recs['Summary'] = self.summaries[str(scotch_idx)]