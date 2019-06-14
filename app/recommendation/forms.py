from django import forms
from .models import State

class StateForm(forms.ModelForm):

	class Meta:
		model = State
		fields = ('name',)
		labels = {'name' : ('')}



'''
class StateForm(forms.Form):
	state = forms.CharField(label='How are you feeling today?', 
							max_length=50, 
							required=False)
'''