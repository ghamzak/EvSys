import json, re, sys, random # pickle
from random import shuffle
from django.conf import settings
with open(settings.QUALIA_DATA_DICT, 'r') as infile:
    data = json.load(infile)




# with open('/Users/ghamzak/PycharmProjects/OntologyMapping/obj/'+'telicFinal' + '.pkl', 'rb') as f:
# 	telicset = pickle.load(f)
# with open('/Users/ghamzak/PycharmProjects/OntologyMapping/obj/'+'constitutiveTest' + '.pkl', 'rb') as f2:
# 	constitutiveset = pickle.load(f2)
# with open('/Users/ghamzak/PycharmProjects/OntologyMapping/obj/'+'agentiveFinal' + '.pkl', 'rb') as f1:
# 	agentiveset = pickle.load(f1)

# with open('/Users/ghamzak/PycharmProjects/OntologyMapping/obj/teldoc.pkl', 'rb') as s1:
# 	teldoc = pickle.load(s1)

# with open('/Users/ghamzak/PycharmProjects/OntologyMapping/obj/agedoc.pkl', 'rb') as s2:
# 	agedoc = pickle.load(s2)

# with open('/Users/ghamzak/PycharmProjects/OntologyMapping/obj/condoc.pkl', 'rb') as s3:
# 	condoc = pickle.load(s3)

# functions
def grabentry(lex, quale):
	for k, v in data.items():
		if v['lex'] == lex and v['quale'] == quale:
			return k
	return -1

def annotate(entry, annotation, user):
	data[entry]['annotations'] = (user, annotation)
	return
def takeComment(entry, comment, user):
	data[entry]['comment'] = (user, comment)
	return

def paginateTelic(telset):
	telicdict = {}	
	
	for i in range(1,(len(telset)//25)+1):
		attentionTest = []
		up = 25*i
		down = up - 25
		pageContent = []
		for k, v in enumerate(telset):
			if k < up and k >= down:
				pageContent.append(v)
		for at in range(3):
			keyindex = random.randint(0, len(telset)-1)
			if len(telset) > keyindex + 30:
				valueindex = keyindex + 30
			else:
				valueindex = keyindex - 30
			attentionTest.append((telset[keyindex][0], telset[valueindex][1], 'AttentionTest'))
		pageContent += attentionTest
		shuffle(pageContent)
		telicdict[str(i)] = pageContent
	return telicdict

def paginateAgentive(agenset):
	agendict = {}	
	for i in range(1,(len(agenset)//25)+1):
		attentionTest = []
		up = 25*i
		down = up - 25
		pageContent = []
		for k, v in enumerate(agenset):
			if k < up and k >= down:
				pageContent.append(v)
		for at in range(3):
			keyindex = random.randint(0, len(agenset)-1)
			if len(agenset) > keyindex + 30:
				valueindex = keyindex + 30
			else:
				valueindex = keyindex - 30
			attentionTest.append((agenset[keyindex][0], agenset[valueindex][1], 'AttentionTest'))
		pageContent += attentionTest
		shuffle(pageContent)
		agendict[str(i)] = pageContent
	return agendict

def paginateConstitutive(conset):
	shuffle(conset)
	condict = {}	
	for i in range(1,(len(conset)//25)+1):
		attentionTest = []
		up = 25*i
		down = up - 25
		pageContent = []
		for k, v in enumerate(conset):
			if k < up and k >= down:
				pageContent.append(v)
		for at in range(3):
			keyindex = random.randint(0, len(conset)-1)
			if len(conset) > keyindex + 30:
				valueindex = keyindex + 30
			else:
				valueindex = keyindex - 30
			attentionTest.append((conset[keyindex][0], conset[valueindex][1], 'AttentionTest'))
		pageContent += attentionTest
		shuffle(pageContent)
		condict[str(i)] = pageContent
	return condict





def saveToLexicon(data):
	with open(settings.QUALIA_DATA_DICT, 'w') as fout:
		json.dump(data, fout, ensure_ascii=True)








