import json


def confirmationLoop(func):
    confirmed  = False
    while not confirmed:
        func()
        confirmed = raw_input('Is this the expected value? (y/n) ') == 'y'

def printDifferentiated(title, strings):
    print title
    for string in strings:
        print '\t|%s' % string.rstrip()


class CodeFile(object):
    def __init__(self, repo_path, filename):
        self._filename = filename
        self._sample = {}

        with open(repo_path + self._filename, 'r') as code_file:
            self._code_lines = code_file.readlines()

    def extractSample(self):
        self._sample = { 'related_lines': {}, 'documentation': {} }
        self._sample['filename'] = self._filename

        confirmationLoop(self._getSnippet)
        confirmationLoop(self._getDescription)

        match_string = raw_input('Enter the start of the substring to match followed by an elipsis '
                                 'and the end of the substring to match: ')
        while match_string:
            self._addMatch(match_string)
            match_string = raw_input('Enter another match string, or nothing to finish: ')

        return self._sample

    def _getSnippet(self):
        snippet_start = int(raw_input('Enter the number of the first line in the snippet: '))
        snippet_end = int(raw_input('Enter the number of the last line in the snippet: '))
        snippet_lines = self._code_lines[snippet_start - 1:snippet_end]

        printDifferentiated('Selected snippet:', [snippet_lines[0], '...', snippet_lines[-1]])

        self._sample['start_line'] = snippet_start
        self._sample['snippet_lines'] = snippet_lines

    def _getDescription(self):
        description_or_line = raw_input(
                'Enter the first line number of the description, or the description itself: ')
        try:
            first_line = int(description_or_line)
            last_line = int(raw_input('Enter the last line number of the description: '))
            self._sample['description'] = '\n'.join(self._code_lines[first_line - 1:last_line])
        except ValueError:
            self._sample['description'] = description_or_line

        printDifferentiated('Selected description:', [self._sample['description']])

    def _addMatch(self, match_string):
        match_key = self._getMatchKey(match_string)
        related_lines = self._getRelatedLines()

        if raw_input('Is this acceptable? (y/n)') == 'y':
            self._sample['related_lines'][match_key] = related_lines

    def _getMatchKey(self, match_string):
        match_components = match_string.lower().split('...')
        lowercase_description = self._sample['description'].lower()
        match_start = lowercase_description.find(match_components[0])

        # Offset match end so that index points to character after last.
        match_end = lowercase_description.find(match_components[1], match_start)
        match_end += len(match_components[1])

        printDifferentiated('Description substring:', [self._sample['description'][match_start:match_end]])

        return '%d,%d' % (match_start, match_end)

    def _getRelatedLines(self):
        match_string = raw_input(
                'Enter the lines or ranges (two line numbers separated by a dash)'
                'of code that relate to this part of the description.'
                'Separate items with commas: ')
        match_string = match_string.replace(' ', '')
        split_match_string = match_string.split(',')

        related_lines = []
        print 'Relating lines:'
        for el in split_match_string:
            if '-' in el:
                split_range = el.split('-')
                range_start = int(split_range[0]) - self._sample['start_line']
                range_end = (int(split_range[1]) - self._sample['start_line']) + 1
                related_lines.extend(range(range_start, range_end))

                printDifferentiated('', [self._sample['snippet_lines'][range_start], '...', self._sample['snippet_lines'][range_end -1]])
            else:
                line_index = int(el) - self._sample['start_line']
                related_lines.append(line_index)

                printDifferentiated('', [self._sample['snippet_lines'][line_index]])

        return related_lines


def main():
    project_name = raw_input('Enter project name: ')
    output_file = 'repo_data/%s.json' % project_name
    repo_dir = 'repos/%s/' % project_name

    with open(output_file, 'r') as f:
        project_data = json.loads(f.read())

    if raw_input('Overwrite existing samples instead of appending? (y/n)') == 'y':
        print 'overwriting'
        samples = []
    else:
        samples = project_data['samples']

    current_filename = raw_input('Enter file name relative to repo root (or nothing to quit): ')
    while current_filename:
        code_file = CodeFile(repo_dir, current_filename)

        continue_with_file = True
        while continue_with_file:
            try:
                samples.append(code_file.extractSample())

                with open(output_file, 'w') as f:
                    project_data['samples'] = samples
                    f.write(json.dumps(project_data))
                    print 'json dumped to file'
                    print 'Number of recorded samples: %d' % len(samples)
            except Exception as e:
                print 'Encountered error while extracting sample: %s' % e

            continue_with_file = raw_input('Do you want to continue with this file? (y/n) ') == 'y'
        current_filename = raw_input('Enter file name relative to repo root (or nothing to quit): ')



if __name__ == '__main__':
    main()
