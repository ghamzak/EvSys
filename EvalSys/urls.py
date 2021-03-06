from django.conf.urls import url, include
from EvalSys.views import *


urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^Telic/1$', Telic1.as_view(), name='telic1'),
	url(r'^Telic/2$', Telic2.as_view(), name='telic2'),
	url(r'^Telic/3$', Telic3.as_view(), name='telic3'),
	url(r'^Telic/4$', Telic4.as_view(), name='telic4'),
	url(r'^Telic/5$', Telic5.as_view(), name='telic5'),
	url(r'^Telic/6$', Telic6.as_view(), name='telic6'),
	url(r'^Telic/7$', Telic7.as_view(), name='telic7'),
	url(r'^Telic/8$', Telic8.as_view(), name='telic8'),
	url(r'^Telic/9$', Telic9.as_view(), name='telic9'),
	url(r'^Telic/10$', Telic10.as_view(), name='telic10'),
	url(r'^Telic/11$', Telic11.as_view(), name='telic11'),
	url(r'^Telic/12$', Telic12.as_view(), name='telic12'),
	url(r'^Telic/13$', Telic13.as_view(), name='telic13'),
	url(r'^Telic/14$', Telic14.as_view(), name='telic14'),
	url(r'^Telic/15$', Telic15.as_view(), name='telic15'),
	url(r'^Telic/16$', Telic16.as_view(), name='telic16'),
	url(r'^Telic/17$', Telic17.as_view(), name='telic17'),
	url(r'^Telic/18$', Telic18.as_view(), name='telic18'),
	url(r'^Telic/19$', Telic19.as_view(), name='telic19'),
	url(r'^Telic/20$', Telic20.as_view(), name='telic20'),
	url(r'^Telic/21$', Telic21.as_view(), name='telic21'),
	url(r'^Telic/22$', Telic22.as_view(), name='telic22'),
	url(r'^Telic/23$', Telic23.as_view(), name='telic23'),
	url(r'^Telic/24$', Telic24.as_view(), name='telic24'),
	url(r'^Telic/25$', Telic25.as_view(), name='telic25'),
	url(r'^Telic/26$', Telic26.as_view(), name='telic26'),
	url(r'^Telic/27$', Telic27.as_view(), name='telic27'),
	url(r'^Telic/28$', Telic28.as_view(), name='telic28'),
	url(r'^Telic/29$', Telic29.as_view(), name='telic29'),
	url(r'^Telic/30$', Telic30.as_view(), name='telic30'),
	url(r'^Telic/31$', Telic31.as_view(), name='telic31'),
	url(r'^Telic/32$', Telic32.as_view(), name='telic32'),
	url(r'^Telic/33$', Telic33.as_view(), name='telic33'),
	url(r'^Telic/34$', Telic34.as_view(), name='telic34'),
	url(r'^Telic/35$', Telic35.as_view(), name='telic35'),
	url(r'^Agentive/1$', Agentive1.as_view(), name='agentive1'),
	url(r'^Agentive/2$', Agentive2.as_view(), name='agentive2'),
	url(r'^Agentive/3$', Agentive3.as_view(), name='agentive3'),
	url(r'^Agentive/4$', Agentive4.as_view(), name='agentive4'),
	url(r'^Agentive/5$', Agentive5.as_view(), name='agentive5'),
	url(r'^Constitutive/1$', Constitutive1.as_view(), name='constitutive1'),
	url(r'^Constitutive/2$', Constitutive2.as_view(), name='constitutive2'),
	url(r'^Constitutive/3$', Constitutive3.as_view(), name='constitutive3'),
	url(r'^Constitutive/4$', Constitutive4.as_view(), name='constitutive4'),
	url(r'^Constitutive/5$', Constitutive5.as_view(), name='constitutive5'),
	url(r'^Constitutive/6$', Constitutive6.as_view(), name='constitutive6'),
	url(r'^Constitutive/7$', Constitutive7.as_view(), name='constitutive7'),
	url(r'^Constitutive/8$', Constitutive8.as_view(), name='constitutive8'),
	url(r'^Constitutive/9$', Constitutive9.as_view(), name='constitutive9'),
	url(r'^Constitutive/10$', Constitutive10.as_view(), name='constitutive10'),
	url(r'^Constitutive/11$', Constitutive11.as_view(), name='constitutive11'),
	url(r'^Constitutive/12$', Constitutive12.as_view(), name='constitutive12'),
	url(r'^Constitutive/13$', Constitutive13.as_view(), name='constitutive13'),
	url(r'^Constitutive/14$', Constitutive14.as_view(), name='constitutive14'),
	url(r'^Constitutive/15$', Constitutive15.as_view(), name='constitutive15'),
	url(r'^Constitutive/16$', Constitutive16.as_view(), name='constitutive16'),
	url(r'^Constitutive/17$', Constitutive17.as_view(), name='constitutive17'),
	url(r'^Constitutive/18$', Constitutive18.as_view(), name='constitutive18'),
	url(r'^Constitutive/19$', Constitutive19.as_view(), name='constitutive19'),
	url(r'^Constitutive/20$', Constitutive20.as_view(), name='constitutive20'),
	url(r'^Constitutive/21$', Constitutive21.as_view(), name='constitutive21'),
	url(r'thanks/', ThanksView.as_view(), name='thanks'),
]
