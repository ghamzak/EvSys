from django import forms
from EvalSys.models import Qualia
# from django.forms.models import inlineformset_factory

class HomeForm(forms.ModelForm):
	"""docstring for HomeForm"""
	reasonable = forms.BooleanField(required=False)

	class Meta:
		"""docstring for ClassName"""
		model = Qualia
		fields = [
		'reasonable',
		]

class IndexForm(forms.Form):
	user = forms.CharField(max_length=2, required=True)