import json

with open('all_samples.json', 'r') as f:
    samples = json.loads(f.read())

for sample in samples:
    indent_length = len(sample['snippet_lines'][0]) - len(sample['snippet_lines'][0].lstrip())
    for i in range(len(sample['snippet_lines'])):
        sample['snippet_lines'][i] = sample['snippet_lines'][i][indent_length:]

with open('all_samples.json', 'w') as f:
    print len(samples)
    f.write(json.dumps(samples))
