import json

with open('positive_samples.json', 'r') as f:
    positive_samples = json.loads(f.read())
with open('generated_samples.json', 'r') as f:
    generated_samples = json.loads(f.read())

for sample in generated_samples:
    snippet_sample = positive_samples[int(sample.split(':')[0])]
    for key in snippet_sample['related_lines']:
        generated_samples[sample]['related_lines'][key] = []

with open('generated_samples.json', 'w') as f:
    print len(generated_samples)
    f.write(json.dumps(generated_samples))
