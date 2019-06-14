from django.db import models
from django.conf import settings

class State(models.Model): # user/state database

	# record emotional state
	name = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.name

class Scotch(models.Model): # database of scotch name/age

	name = models.CharField(max_length=100, blank=True, unique=False)
	age = models.CharField(max_length=50, blank=True, null=True, unique=False)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'Scotch'


class EmotionSyn(models.Model): # database of emotions and synonyms
	
	# Parent emotion is the emotion that was used to generate a list of synonyms
	# In this case, a master emotion is mapped with a list of synonyms.
	# If the user state is not in a list of synonyms, it will be used to
	# compute a similarity score between the state and master emotion in views.py
	parent_emotion = models.CharField(max_length=50)
	synonyms = models.TextField()

class EmotionScotchSimilarity(models.Model): # database of emotion-scotch similarity scores

	similarity = models.TextField(blank=True)

	class Meta:
		db_table = 'Similarity'

class Summaries(models.Model):

	summary = models.TextField(blank=True)