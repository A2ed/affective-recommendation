from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import ast
import random

from .forms import StateForm
from .scotchy import *
from .models import State, Scotch, EmotionScotchSimilarity


def home(request):
	# initialize emotional state
	initial={'emotional_state': request.session.get('emotional_state', None)}
	# do this when posted
	if request.method == 'POST':
		# use  form to get user's emotional state
		form = StateForm(request.POST)
		if form.is_valid():
			# save to state model
			form.save()
			# record emotional state
			request.session['emotional_state'] = form.cleaned_data['name']
			# redirect to new view showing recommendations
			return redirect('results')
			#return HttpResponseRedirect(reverse('results'))
	else:
		form = StateForm()
	return render(request, 'recommendation/home.html', {'form' : form})

def results(request):
	emotional_state = request.session['emotional_state']
	# initiate recommendation engine
	recs = RecommendationEngine()
	# get scotch recommendation idx based on emotion
	idx = recs.get_rec(emotional_state)
	# select scotch data from SQL database
	rec = Scotch.objects.get(id=idx+1)
	# get summaries for recommended scotch
	adjs = ast.literal_eval(Summaries.objects.get(id=idx+1).summary)
	# if more than three adjectives, randomly sample three from the list
	if len(adjs) > 3:
			adjs = random.sample(adjs, 3)
	else:
		pass

	if len(rec.age) > 1:
		context = {'emotion' : emotional_state,
					'rec1_name' : rec.name,
					'rec1_age' : rec.age,
					'rec1_sum' : '. '.join(adjs) + '.'}
	else:
		context = {'emotion' : emotional_state,
					'rec1_name' : rec.name,
					'rec1_sum' : '. '.join(adjs) + '.'}
	return render(request, 'recommendation/results.html', context)
