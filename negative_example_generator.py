import copy
import random
import json
import os

with open('all_samples.json', 'r') as f:
    all_samples = json.loads(f.read())
with open('generated_samples.json', 'r') as f:
    generated_samples = json.loads(f.read())

while True:
    os.system('clear')

    first = random.randint(0, len(all_samples) - 1)
    last = random.randint(0, len(all_samples) - 1)
    key = '%d:%d' % (first, last)

    if key in generated_samples:
        continue

    print '%d Total Examples\n' % len(generated_samples)

    snippet_sample = all_samples[first]
    description_sample = all_samples[last]
    
    merged_sample = copy.deepcopy(snippet_sample)
    merged_sample['description'] = description_sample['description']
    merged_sample['related_lines'] = {}

    print 'Description:\n%s' % merged_sample['description']
    print 'Snippet:\n%s' % ''.join(merged_sample['snippet_lines'])
    status = raw_input('Ok? ((y)/n) ')

    if first == last:
        continue

    if status != 'n':
        generated_samples[key] = merged_sample

    status = raw_input('Write? (y/(n)) ')
    if status == 'y':
        with open('generated_samples.json', 'w') as f:
            f.write(json.dumps(generated_samples))
