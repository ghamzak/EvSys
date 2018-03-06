from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeForm, IndexForm, CommentBox, AnnotationFormSet, AnnotationForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import render_to_string
# import json, re
from django.conf import settings
# from .models import Qualia
# from django.db.models import Q
import json, re, sys, random # pickle
from random import shuffle
from .myfunctions import *


with open(settings.QUALIA_DATA_DICT, 'r') as infile:
    data = json.load(infile)


class IndexView(TemplateView):
	"""docstring for IndexView"""
	template_name = 'EvalSys/index.html'

	def get(self, request, *args, **kwargs):
		userform = IndexForm()
		args = {'userform': userform}
		return render(request, self.template_name, args)
	def post(self, request, *args, **kwargs):
		userlist = {'sb': 'Susan', 'cb': 'Claire', 'gk': 'Ghazaleh'}
		userform = IndexForm(request.POST)
		if userform.is_valid():
			print('form is valid')
			uservar = userform.cleaned_data.get('user')

			if uservar in userlist.keys():
				print('User is authenticated.')
				user_name = userlist[uservar]
				request.session['user_name'] = uservar
				print(request.session['user_name'])
				return HttpResponseRedirect('thanks')
			else:
				user_name = ''
				return HttpResponse('Sorry! You are not an authenticated user!')

class ThanksView(TemplateView):
	"""docstring for ClassName"""
	template_name = 'EvalSys/thanks.html'
	def get(self, request):
		return render(request, self.template_name)


class Telic1(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1,26)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(1,26)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)
				

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks') #render(request, self.template_name, args)

class Telic2(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(26,51)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(26,51)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)
			 	

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks') #render(request, self.template_name, args)

class Telic3(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(51,76)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(51,76)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks') #render(request, self.template_name, args)

class Telic4(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(76,101)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(76,101)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic5(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(101,126)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(101,126)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic6(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(126,151)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(126,151)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic7(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(151,176)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(151,176)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic8(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(176,201)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(176,201)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic9(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(201,226)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(201,226)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic10(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(226,251)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(226,251)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic11(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(251,276)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(251,276)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic12(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(276,301)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			print(user_judgment)
			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)

			indeces1 = [str(i) for i in range(276,301)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }


			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic13(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(301,326)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(301,326)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic14(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(326,351)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(326,351)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic15(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(351,376)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(351,376)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic16(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(376,401)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(376,401)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic17(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(401,426)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(401,426)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic18(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(426,451)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(426,451)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic19(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(451,476)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(451,476)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic20(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(476,501)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(476,501)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic21(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(501,526)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(501,526)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic22(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(526,551)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(526,551)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic23(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(551,576)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(551,576)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic24(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(576,601)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(576,601)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic25(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(601,626)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(601,626)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic26(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(626,651)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(626,651)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic27(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(651,676)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(651,676)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic28(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(676,701)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(676,701)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic29(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(701,726)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(701,726)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic30(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(726,751)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(726,751)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic31(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(751,776)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(751,776)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic32(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(776,801)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(776,801)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic33(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(801,826)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(801,826)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic34(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(826,851)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(826,851)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Telic35(DetailView):
	template_name = 'EvalSys/qualia_detail.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(851,869)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(851,869)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Agentive1(DetailView):
	template_name = 'EvalSys/qualia_detail_agentive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(869,869+25)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(869,869+25)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Agentive2(DetailView):
	template_name = 'EvalSys/qualia_detail_agentive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(894,894+25)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(894,894+25)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Agentive3(DetailView):
	template_name = 'EvalSys/qualia_detail_agentive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(919,944)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(919,944)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Agentive4(DetailView):
	template_name = 'EvalSys/qualia_detail_agentive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(944,969)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(944,969)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Agentive5(DetailView):
	template_name = 'EvalSys/qualia_detail_agentive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(969,981)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(969,981)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive1(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(981,1006)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(981,1006)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive2(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1006,1031)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1006,1031)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive3(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1031,1056)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1031,1056)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive4(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1056,1081)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1056,1081)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive5(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1081,1106)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1081,1106)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive6(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1106,1131)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1106,1131)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive7(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1131,1156)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1131,1156)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive8(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1156,1181)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1156,1181)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive9(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1181,1206)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1181,1206)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive10(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1206,1231)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1206,1231)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive11(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1231,1256)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1231,1256)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive12(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1256,1281)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1256,1281)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive13(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1281,1306)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1281,1306)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive14(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1306,1331)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1306,1331)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive15(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1331,1356)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1331,1356)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive16(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1356,1381)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1356,1381)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive17(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1381,1406)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1381,1406)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive18(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1406,1431)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1406,1431)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive19(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1431,1456)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1431,1456)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive20(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1456,1481)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1456,1481)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')

class Constitutive21(DetailView):
	template_name = 'EvalSys/qualia_detail_constitutive.html'
	def get(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			# print(user)
			form = HomeForm()
			comment = CommentBox()
			indeces1 = [str(i) for i in range(1481,1513)]
			obj = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'
			# print(user_judgment)			
			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			}
			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				if j[user_judgment]: # and re.findall(user, j[user_judgment])
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]: # and re.findall(user, j['comment'])
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': form, 'entries': obj , 'object': obj2, 'formset': formset}
			return render(request, self.template_name, args)

	def post(self, request, *args, **kwargs):
		user = request.session['user_name']
		if not user:
			return HttpResponse('Please Start Enter Your Username First')
		else:
			judgementform = HomeForm(request.POST)
			commentform = CommentBox(request.POST)
			indeces1 = [str(i) for i in range(1481,1513)]
			obj = []
			keys = []
			for i, j in data.items():
				if i in indeces1:
					obj.append(j)
					keys.append(i)
			user_judgment = user + '-judgment'
			user_comment = user + '-comment'

			obj2 = [(i['lex'], i['quale'], i['doc']) for i in obj]

			formsetfeed = {
			'form-TOTAL_FORMS': '28',
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': ''
			 }

			for i, j in enumerate(obj):
				commentfield = 'form-' + str(i) + '-comment'
				judgementfield = 'form-' + str(i) + '-judgement'
				data[keys[i]][user_judgment] = request.POST[judgementfield]
				data[keys[i]][user_comment] = request.POST[commentfield]

				saveToLexicon(data)

				if j[user_judgment]:
					formsetfeed[judgementfield] = j[user_judgment]
				else:
					formsetfeed[judgementfield] = 'idk'
				if j[user_comment]:
					formsetfeed[commentfield] = j[user_comment]
				else:
					formsetfeed[commentfield] = ''

			formset = AnnotationFormSet(formsetfeed)
			args = {'form': judgementform, 'entries': obj , 'object': obj2, 'formset': formset}
			return HttpResponseRedirect('thanks')








