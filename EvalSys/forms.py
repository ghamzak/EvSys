from django import forms
from django.forms import formset_factory
from EvalSys.models import Qualia
# from django.forms.models import inlineformset_factory

class AnnotationForm(forms.Form):
	# entity = forms.CharField(required=True, max_length=100)
	# quale = forms.CharField(max_length=500)
	# doc = forms.CharField(max_length=590)
	judgement = forms.CharField(required=True, max_length=3)
	comment = forms.CharField(required=False, widget=forms.Textarea)

AnnotationFormSet = formset_factory(AnnotationForm)

class HomeForm(forms.Form):
	"""docstring for HomeForm"""
	judgement = forms.CharField(required=True, max_length=3)
	# comment = forms.CharField(required=False, widget=forms.Textarea)
	# reasonable = forms.BooleanField(required=False)
	# unreasonable = forms.BooleanField(required=False)
	# IDK = forms.BooleanField(required=False)
	# class Meta:
	# 	"""docstring for ClassName"""
	# 	model = Qualia
	# 	fields = [
	# 	'reasonable',
	# 	]

class IndexForm(forms.Form):
	user = forms.CharField(max_length=2, required=True)

class CommentBox(forms.Form):
	comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Insert Your Comments Here.'}))



