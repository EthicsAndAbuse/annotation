import json, sys
import os


infile = sys.argv[1]
annotator = sys.argv[2]
start_conversation = 0
if len(sys.argv) == 4:
	start_conversation = int(sys.argv[3])

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

if start_conversation > 0:
	print('You want to start from {}.'.format(start_conversation))

if len(tagged_conversations) != start_conversation:
	print('The start number provided is not correct or your data is wrong')
	sys.exit()

print('\n')

def write_to_disk(outfile_name):
	with open(outfile_name, 'w') as outfile:
		json.dump(tagged_conversations, outfile)

def annotate_utterance(utterance):
	# print(utterance['utterance'])

	compressed = ''.join(c.lower() for c in utterance['utterance'] if not c.isspace())

	if compressed in clean:
		utterance['tag'] = 'nonabusive'
		counts['skipped'] +=1
		print('utterance seen before, skipping...')
	elif compressed in offensive:
		utterance['tag'] = 'offensive'
		counts['skipped'] +=1
		print('utterance seen before, skipping...')
	elif compressed in hatespeech:
		utterance['tag'] = 'hatespeech'
		counts['skipped'] +=1
		print('utterance seen before, skipping...')
	else:
		cmd = ''
		while cmd not in ['1','2','3','4','q']:
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
				write_to_disk(outfile_name)
				sys.exit()
			else:
				print('wrong command')
			print('')

	utterance['annotator'] = annotator
	write_to_disk(outfile_name)
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


conversation = start_conversation
while (counts['clean'] + counts['offensive'] + counts['hate'] + counts['nonsense']) < annotated_count:
	utterance_count = 0
	print('*** New dialogue, which has a pretag of: ' + d[conversation]['pretag'] + ' ***')
	#make sure that the hate and offensive are annotated first and put into the output array
	if d[conversation]['pretag'] == 'hatespeech':
		d[conversation],utterance_count = annotate_conversation(d[conversation])
	elif d[conversation]['pretag'] == 'offensive':
		d[conversation],utterance_count = annotate_conversation(d[conversation])
	elif d[conversation]['pretag'] == 'clean':
		d[conversation],utterance_count = annotate_conversation(d[conversation])
	#annotated_count -= utterance_count
	tagged_conversations.append( d[conversation])
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




