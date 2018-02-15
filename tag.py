import json, sys
infile = sys.argv[1]
outfile = sys.argv[2]
annotator = sys.argv[3]

print('\n')

clean = []
offensive = []
hatespeech = []

counts = {'offensive':0,'hate':0,'clean':0,'nonsense':0}

def annotate_utterance(utterance):
	# print(utterance['utterance'])
	
	compressed = ''.join(c.lower() for c in utterance['utterance'] if not c.isspace())
	
	if compressed in clean:
		utterance['tag'] = 'nonabusive'
	elif compressed in offensive:
		utterance['tag'] = 'offensive'
	elif compressed in hatespeech:
		utterance['tag'] = 'hatespeech'
	else:
		cmd = ''
		while cmd not in ['1','2','3','4']:
			print('')
			cmd = input('choose 1 = non abusive, 2 = offensive, 3 = hate, 4 = nonsense\n')
			if (cmd == '1'):
				utterance['tag'] = 'nonabusive'
				clean.append(compressed)
				counts['clean'] += 1
			elif (cmd == '2'):
				utterance['tag'] = 'offensive'
				offensive.append(compressed)
				counts['offensive'] += 1
			elif (cmd == '3'):
				utterance['tag'] = 'hatespeech'
				hatespeech.append(compressed)
				counts['hate'] += 1
			elif (cmd =='4'):
				utterance['tag'] = 'nonsense'
				counts['nonsense'] += 1
			else:
				print('wrong command')
			print('')

	utterance['annotator'] = annotator

	return utterance

def annotate_conversation(conversation):
	utterance_count = 0
	for utterance in conversation['dialogue']:
		if utterance['actor'] != u'user':
			print('     <-bot-> ' + utterance['utterance']) # +'\n')
		else:
			print('<-usr-> '+utterance['utterance']) # +'\n')
			if utterance['pretag'] != 'clean':
				utterance = annotate_utterance(utterance)
				utterance_count += 1
	return conversation, utterance_count

with open(infile) as json_data:
    data = json.load(json_data)

d = data['hatespeech'] + data['offensive']

annotated_count = 200
i = 0

tagged_conversations = []

while i < annotated_count:
	utterance_countt = 0
	print('*** New dialogue, which has a pretag of: ' + d[i]['pretag'] + ' ***')
	if d[i]['pretag'] == 'hatespeech':
		d[i],utterance_count = annotate_conversation(d[i])
		tagged_conversations.append( d[i])
		i += utterance_count
	elif d[i]['pretag'] == 'offensive':
		d[i],utterance_count = annotate_conversation(d[i])
		tagged_conversations.append( d[i])
		i += utterance_count
	print('')
	print('End of dialogue. Update of utterance counts:')
	print('Nonsense count: ' + str(counts['nonsense']) + '  Clean count: ' + str(counts['clean']))
	print('Offensive count: ' + str(counts['offensive']) + '  Hate speech count: ' + str(counts['hate']))
	print('Totaling: ' + str(counts['clean'] + counts['offensive'] + counts['hate'] + counts['nonsense']))
	print('')
	if i != (annotated_count - 1):
		input('Press Enter to continue...')


print('')
print('End of annotation. Utterance annotated:')
print('Nonsense count: ' + str(counts['nonsense']) + '  Clean count: ' + str(counts['clean']))
print('Offensive count: ' + str(counts['offensive']) + '  Hate speech count: ' + str(counts['hate']))
print('Totaling: ' + str(counts['clean'] + counts['offensive'] + counts['hate'] + counts['nonsense']))
print('')

with open(outfile, 'w') as outfile:
    json.dump(d, outfile)