"""
Finds all links to github repositories in the awesome-python readme and randomly
chooses NUM_REPOS from the list of links.
"""

import re
import random


NUM_REPOS = 50
README_PATH = 'awesome_python_readme.md'
OUTPUT_PATH = 'sampled_repos'

with open(README_PATH, 'r') as readme:
    readme_text = readme.read()

github_urls = re.findall('(https?:\/\/github\.com\/.*?)\)', readme_text)
sampled_urls = random.sample(github_urls, NUM_REPOS)

with open(OUTPUT_PATH, 'w') as output:
    output.write('\n'.join(sampled_urls))
