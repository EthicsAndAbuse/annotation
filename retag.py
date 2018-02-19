import json, sys
import os

annotator = sys.argv[1]

outfile_name = 'annotated_' + annotator + '.json'

clean = []
offensive = []
hatespeech = []
tagged_conversations = []

counts = {'offensive':0,'hate':0,'clean':0,'nonsense':0, 'skipped':0}

if os.path.isfile(outfile_name) :
	with open(outfile_name, 'r') as outfile:
		tagged_conversations = json.load(outfile)

if len(tagged_conversations):
	print('Loaded {} conversations from {}'.format(len(tagged_conversations),outfile_name))

print('\n')

def write_to_disk(outfile_name):
	with open(outfile_name, 'w') as outfile:
		json.dump(tagged_conversations, outfile)

def annotate_utterance(utterance):
	# print(utterance['utterance'])

	compressed = ''.join(c.lower() for c in utterance['utterance'] if not c.isspace())
	if 'tag' in utterance and utterance['tag'] in ['nonabusive', 'nonsense']:
		write_to_disk(outfile_name)
		return utterance

	if compressed in clean:
		utterance['tag'] = 'nonabusive'
		counts['skipped'] +=1
		print('utterance seen before, skipping...')
	elif compressed in offensive:
		utterance['tag'] = 'offensive'
		counts['skipped'] +=1
		print('utterance seen before, skipping...')
	elif compressed in hatespeech:
		utterance['tag'] = 'sexual/hate'
		counts['skipped'] +=1
		print('utterance seen before, skipping...')
	else:
		cmd = ''
		while cmd not in ['1','2','3','4']:
			print('')
			cmd = raw_input('choose 1 = non abusive, 2 = offensive, 3 = sexual/hate, 4 = nonsense, q = save to disk and quit\n')
			if (cmd == '1'):
				utterance['tag'] = 'nonabusive'
				clean.append(compressed)
				counts['clean'] += 1
			elif (cmd == '2'):
				utterance['tag'] = 'offensive'
				offensive.append(compressed)
				counts['offensive'] += 1
			elif (cmd == '3'):
				utterance['tag'] = 'sexual/hate'
				hatespeech.append(compressed)
				counts['hate'] += 1
			elif (cmd =='4'):
				utterance['tag'] = 'nonsense'
				counts['nonsense'] += 1
			elif (cmd == 'q'):
				print('quitting... file saved in current state')
				write_to_disk(outfile_name)
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

for conversation in range(0, len(tagged_conversations)):
	utterance_count = 0
	print('*** New dialogue, which has a pretag of: ' + tagged_conversations[conversation]['pretag'] + ' ***')
	#make sure that the hate and offensive are annotated first and put into the output array
	tagged_conversations[conversation],utterance_count = annotate_conversation(tagged_conversations[conversation])
	write_to_disk(outfile_name)
	print('')
	print('End of dialogue. Update of utterance counts:')
	print('Nonsense count: ' + str(counts['nonsense']) + '  Clean count: ' + str(counts['clean']))
	print('Offensive count: ' + str(counts['offensive']) + '  Hate speech count: ' + str(counts['hate']))
	print('Skipped count: ' + str(counts['skipped']))
	print('Totaling: ' + str(counts['skipped'] + counts['clean'] + counts['offensive'] + counts['hate'] + counts['nonsense']))
	print('Tagged conversation Num: {}'.format(conversation))
	print('')
	conversation +=1


print('')
print('Last Tagged conversation Num: {}\n'.format((conversation-1)))




