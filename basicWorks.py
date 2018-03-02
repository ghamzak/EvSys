import json, re, sys

# with open(settings.QUALIA_DATA_DICT, 'r') as infile:
#     data = json.load(infile)

# def saveToLexicon(data):
# 	with open('QualiaDictionary.json', 'w') as f:
# 		json.dump(data)


# with open(settings.LEXICON_DATA_DICT, 'w') as fout:
#         json.dump(request.session['lexicon'], fout, ensure_ascii=True)

#--------------------

# with open('QualiaDictionary.json', 'r') as f1:
# 	data = json.load(f1)

# print(list(data.items())[0])



# for i in data.items():
# 	i[1]['gk-judgment'] = ''
# 	i[1]['sb-judgment'] = ''
# 	i[1]['cb-judgment'] = ''


# newdict = {}

# for i in data.items():
# 	newdict[i[0]] = i[1]

# with open("jdict2.json", 'w') as fout:
#         json.dump(newdict, fout, ensure_ascii=True)


with open('jdict3.json', 'r') as f1:
	data = json.load(f1)

telicCount = 0
telicIndecies = []
constCount = 0
constIndecies = []
agentiveCount = 0
agentiveIndecies = []
for i in data.items():
	if i[1]['quale_type'] == 'Telic': 
		telicCount += 1
		telicIndecies.append(int(i[0]))
	elif i[1]['quale_type'] == 'Constitutive': 
		constCount += 1
		constIndecies.append(int(i[0]))
	elif i[1]['quale_type'] == 'Agentive': 
		agentiveCount +=1
		agentiveIndecies.append(int(i[0]))

print("telicCount:",telicCount)
print("constCount:",constCount)
print("agentiveCount:",agentiveCount)

print("min telic:",min(telicIndecies),'max telic:', max(telicIndecies))
print("min agent:", min(agentiveIndecies), "max agent:", max(agentiveIndecies))
print("min cons:", min(constIndecies), 'max cons:', max(constIndecies))

"""
telicCount: 868  .... needs 35 pages
constCount: 532  .... needs 22 pages
agentiveCount: 112 ...needs 5 pages

"""

# print(112//25)

# for i in range(26,32):
# 	data[str(i)]['gk-judgment'] = 'r'


# for i in data.values():
# 	i['gk-comment'] = ''
# 	i['sb-comment'] = ''
# 	i['cb-comment'] = ''

# print(data['1'])

# with open("jdict3.json", 'w') as fout:
#         json.dump(data, fout, ensure_ascii=True)



# print(list(data.keys())[0])
# print(list(data.values())[1])


# newdict = {}
# for i in data.items():
# 	newdict[int(i[0])] = i[1]

# with open("jdict3.json", 'w') as fout:
#         json.dump(newdict, fout, ensure_ascii=True)




