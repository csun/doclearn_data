import os
import json

with open('positive_samples.json', 'r') as f:
    positive_samples = json.loads(f.read())
with open('generated_samples.json', 'r') as f:
    generated_samples = json.loads(f.read())

for sample in generated_samples:
    positive_samples.append(generated_samples[sample])

with open('all_samples.json', 'w') as f:
    print len(positive_samples)
    f.write(json.dumps(positive_samples))
