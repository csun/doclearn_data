import os
import json

all_files = os.listdir('repo_data')

count = 0
output_list = []
for json_file in all_files:
    with open('repo_data/' + json_file, 'r') as f:
        specific_data = json.loads(f.read())

    for sample in specific_data['samples']:
        count += 1
        sample['repo_url'] = specific_data['repo_url']
        sample['commit_hash'] = specific_data['commit_hash']
        output_list.append(sample)

print '%d Total Samples' % count
with open('all_samples.json', 'w') as f:
    f.write(json.dumps(output_list))
