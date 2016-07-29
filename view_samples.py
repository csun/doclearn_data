import json
import os


def render(sample):
    print 'Description:\n%s\n' % sample['description'] 
    print 'Snippet:\n%s\n' % ''.join(sample['snippet_lines'])

    related_count = 1
    print 'Related lines:'
    for indices in sample['related_lines']:
        split_indices = indices.split(',')
        phrase = sample['description'][int(split_indices[0]):int(split_indices[1])]

        print '\tPhrase [%d]:\n\t\t|%s' % (related_count, phrase)

        print '\tLines [%d]:' % related_count
        for line_num in sample['related_lines'][indices]:
            print '\t\t|%s' % sample['snippet_lines'][line_num]

        related_count += 1


with open('all_samples.json', 'r') as f:
    all_samples = json.loads(f.read())

next_sample = 0
while True:
    os.system('clear')
    print 'Sample #%d/%d' % (next_sample + 1, len(all_samples))
    render(all_samples[next_sample])

    raw_next = raw_input('Enter (n) for next, p for previous, or a sample number: ')
    if raw_next == 'n' or raw_next == '':
        next_sample += 1
    elif raw_next == 'p':
        next_sample -= 1
    else:
        next_sample = int(raw_next) - 1
