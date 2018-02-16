import json, sys
infile = sys.argv[1]
annotator = sys.argv[2]
outfile = 'annotated_' + annotator + '.json'

print('\n')

clean = []
offensive = []
hatespeech = []
tagged_conversations = []

counts = {'offensive':0,'hate':0,'clean':0,'nonsense':0}

def write_to_disk(outfile):
	with open(outfile, 'w') as outfile:
		json.dump(tagged_conversations, outfile)

def annotate_utterance(utterance):
	# print(utterance['utterance'])

	compressed = ''.join(c.lower() for c in utterance['utterance'] if not c.isspace())

	if compressed in clean:
		utterance['tag'] = 'nonabusive'
		print('utterance seen before, skipping...')
	elif compressed in offensive:
		utterance['tag'] = 'offensive'
		print('utterance seen before, skipping...')
	elif compressed in hatespeech:
		utterance['tag'] = 'hatespeech'
		print('utterance seen before, skipping...')
	else:
		cmd = ''
		while cmd not in ['1','2','3','4']:
			print('')
			cmd = raw_input('choose 1 = non abusive, 2 = offensive, 3 = hate, 4 = nonsense, q = save to disk and quit\n')
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
			elif (cmd == 'q'):
				print('quitting... file saved in current state')
				write_to_disk(outfile)
				sys.exit()
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

d = data['hatespeech'] + data['offensive'] + data['clean']

annotated_count = 500


conversation = 0
while annotated_count > 0:
	utterance_count = 0
	print('*** New dialogue, which has a pretag of: ' + d[conversation]['pretag'] + ' ***')
	#make sure that the hate and offensive are annotated first and put into the output array
	if d[conversation]['pretag'] == 'hatespeech':
		d[conversation],utterance_count = annotate_conversation(d[conversation])
		tagged_conversations.append( d[conversation])
	elif d[conversation]['pretag'] == 'offensive':
		d[conversation],utterance_count = annotate_conversation(d[conversation])
	elif d[conversation]['pretag'] == 'clean':
		d[conversation],utterance_count = annotate_conversation(d[conversation])
	annotated_count -= utterance_count
	tagged_conversations.append( d[conversation])
	conversation +=1
	print('')
	print('End of dialogue. Update of utterance counts:')
	print('Nonsense count: ' + str(counts['nonsense']) + '  Clean count: ' + str(counts['clean']))
	print('Offensive count: ' + str(counts['offensive']) + '  Hate speech count: ' + str(counts['hate']))
	print('Totaling: ' + str(counts['clean'] + counts['offensive'] + counts['hate'] + counts['nonsense']))
	print('')



