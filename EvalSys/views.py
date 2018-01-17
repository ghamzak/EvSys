from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeForm, IndexForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import render_to_string
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Qualia
from django.db.models import Q


class IndexView(TemplateView):
	"""docstring for IndexView"""
	template_name = 'EvalSys/index.html'

	def get(self, request, *args, **kwargs):
		userform = IndexForm()
		args = {'userform': userform}
		return render(request, self.template_name, args)
	def post(self, request, *args, **kwargs):
		userlist = {'sb': 'Susan', 'cb': 'Claire'}
		userform = IndexForm(request.POST)
		if userform.is_valid():
			print('form is valid')
			uservar = userform.cleaned_data.get('user')

			if uservar in userlist.keys():
				print('User is authenticated.')
				user_name = userlist[uservar]
				request.session['user_name'] = uservar
				print(request.session['user_name'])
				return HttpResponse('Thank you %s . Please add 1 to the end of URL to see your first task.' % user_name)
			else:
				user_name = ''
				return HttpResponse('Sorry! You are not an authenticated user!')

class ThanksView(TemplateView):
	"""docstring for ClassName"""
	template_name = 'EvalSys/thanks.html'
	def get(self, request):
		return render(request, self.template_name)


class TelicDetailView(DetailView):
	# model = Qualia
	# if request.session['user_name'] == 'sb':
	# 	queryset = Qualia.objects.filter(sb_annotations = False)
	queryset = Qualia.objects.filter(post=False)
	template_name = 'EvalSys/qualia_detail.html'

	def get(self, request, *args, **kwargs):
		if request.session['user_name'] == 'sb':
			queryset = Qualia.objects.filter(sb_annotations = False)
			# form = HomeForm()
			# obj = self.get_object()
			# if obj.pk < 777:
			# 	return render(request, self.template_name, {'form': form, 'object': obj})

		elif request.session['user_name'] == 'cb':
			queryset = Qualia.objects.filter(cb_annotations = False)

		form = HomeForm()

		obj = self.get_object()
		print(obj.node)
		print(obj.pk)
		if obj.pk < 777:
			return render(request, self.template_name, {'form': form, 'object': obj})
		elif obj.pk < 892:
			return render(request, 'EvalSys/qualia_detail_agentive.html', {'form': form, 'object': obj})
		else:
			return render(request, 'EvalSys/qualia_detail_constitutive.html', {'form': form, 'object': obj})


	def post(self, request, *args, **kwargs):
		form = HomeForm(request.POST)
		obj = self.get_object()
		print(obj.post)
		if form.is_valid():
			print(form.cleaned_data.get('reasonable'))
			print(obj.post)
			if request.session['user_name'] == 'sb':
				obj.sb_annotations = form.cleaned_data.get('reasonable')
				print(obj.sb_annotations)
			elif request.session['user_name'] == 'cb':
				obj.cb_annotations = form.cleaned_data.get('reasonable')
				print(obj.cb_annotations)
			# obj.post = form.cleaned_data.get('reasonable')
			# print(obj.post)
			obj.save()
		return HttpResponseRedirect('thanks')


