import json, sys
import pandas as pd

with open(sys.argv[1]) as json_data:
    d = json.load(json_data)

with open('bad.txt') as bad:
	bad_expressions = bad.read().splitlines()

df = pd.read_csv('hatebase.csv')
data = df.to_dict(orient='list')


hate_expressions = data['uncivilised']

hate_dict = {'single':[],'multiple':[]}
bad_dict = {'single':[],'multiple':[]}

for expression in hate_expressions:
	if len(expression.split()) > 1:
		hate_dict['multiple'].append(expression)		
	else:
		hate_dict['single'].append(expression)		
		
for expression in bad_expressions:
	if len(expression.split()) > 1:
		bad_dict['multiple'].append(expression)		
	else:
		bad_dict['single'].append(expression)		

data_size = len(d)

print('Dataset size: ',data_size)

def check_against(utterance, word_dict):
	split_utterance = utterance.split()
	for expression in word_dict['multiple']:
		if expression in utterance:
			print(utterance)
			print(expression+ ' TAGGED')
			return True

	for word in split_utterance:
		if word in word_dict['single']:
			# print(utterance)
			# print(word + ' TAGGED')
			return True

	return False

def show_utterances(utterances):
	for utterance in utterances:
		print(utterance['utterance']+'\n')

def show_conversation(conversation, tag):
	print('Conversation is pretagged as :'+ conversation[tag])
	for utterance in conversation['dialogue']:
		if utterance['actor'] == u'user':
			if utterance[tag] == 'clean':
				print('_______' + utterance['utterance'])
			elif utterance[tag] == 'offensive':
				print('*******' + utterance['utterance'])
			else:
				print('!!!!!!!' + utterance['utterance'])
		else:
			print('<-bot-> ' + utterance['utterance'])

counts = {'offensive':0,'hate':0,'clean':0,'total':0}

result = {'hatespeech':[],'offensive':[],'clean':[]}

for conversation in d:
	hate = False
	offensive = False
	for utterance in conversation['dialogue']:
		if utterance['actor'] == u'user':
			if check_against(utterance['utterance'], hate_dict) == True:
				utterance['pretag'] = 'hatespeech'
				# print('<-wtf->'+ utterance['utterance'])
				hate = True
			else:
				if check_against(utterance['utterance'], bad_dict) == True:
					utterance['pretag'] = 'offensive'
					offensive = True
				else:
					utterance['pretag'] = 'clean'
	if hate == True:
		conversation['pretag'] = 'hatespeech'
		counts['hate'] += 1
		result['hatespeech'].append(conversation)
	elif offensive == True:
		conversation['pretag'] = 'offensive'
		counts['offensive'] += 1
		result['clean'].append(conversation)
	else:
		conversation['pretag'] = 'clean'
		counts['clean'] += 1
		result['clean'].append(conversation)
	counts['total'] +=1
	# print('Done ' + str(counts['total']) + ' of ' + str(data_size))

# with open('filtered_data.json', 'w') as outfile:
#     json.dump(d, outfile)

with open('precategorised_data.json','w') as outfile:
	json.dump(result, outfile)
# print(('utterances: %d')%len(filtered_utterances))


