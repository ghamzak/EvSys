from django.conf.urls import url, include
from EvalSys.views import IndexView, ThanksView, TelicDetailView #, HomeView # ConstitutiveView #AgentiveDetailView # , AgentiveView

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)', TelicDetailView.as_view(), name='detail'),
	url(r'^thanks/', ThanksView.as_view(), name='thanks'),
]