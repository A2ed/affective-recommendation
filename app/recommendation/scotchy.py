import random
import json
import numpy as np
import spacy
import ast

from .models import Scotch, EmotionSyn, EmotionScotchSimilarity, Summaries

class RecommendationEngine():
		

	def match_emotion(self, emotion):
		# dict to store similarity values
		similarity = {}

		for e in EmotionSyn.objects.all():
			# check and see if emotion matches one in dictionary
			if emotion == e.parent_emotion or emotion in ast.literal_eval(e.synonyms):
				# if so, return emotion
				return e.parent_emotion
			else:
				pass

		# if not, calculate similarity between emotion and dictionary
		for e in EmotionSyn.objects.all():
			# initialize English model
			nlp = spacy.load('en_core_web_sm')

			doc1 = nlp(emotion)
			doc2 = nlp(e.parent_emotion)
			similarity[e.parent_emotion] = doc1.similarity(doc2)

			# return max
			return max(similarity, key=similarity.get) 

	def get_rec(self, emotion):

		# get the emotion for recommendation
		self.rec_emotion = self.match_emotion(emotion)
		# get index of emotion
		self.rec_idx = EmotionSyn.objects.get(parent_emotion=self.rec_emotion).pk 
		# extract similarities as list
		similarities = ast.literal_eval(EmotionScotchSimilarity.objects.get(pk=self.rec_idx).similarity)
		# convert to numpy array
		sim_array = np.asarray(similarities)
		# get indices of top three scotches based on precomputed similarity scores
		scotch_idx = random.sample(list(sim_array.argsort()[-25:][::-1]), 1)[0]

		return scotch_idx