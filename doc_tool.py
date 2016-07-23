import json
import os
import sys


def confirmationLoop(func):
    confirmed  = False
    while not confirmed:
        func()
        confirmed = raw_input('Is this the expected value? (y/n) ') == 'y'

def printDifferentiated(title, strings):
    print title
    for string in strings:
        print '\t|%s' % string.rstrip()


def main():
    project_name = raw_input('Enter project name: ')
    output_file = 'repo_data/%s.json' % project_name
    repo_dir = 'repos/%s/' % project_name

    sys.path.append(os.path.join(os.path.dirname(__file__), repo_dir))

    with open(output_file, 'r') as f:
        project_data = json.loads(f.read())

    for sample in project_data['samples']:
        print 'Reading next sample from %s at line %d' % (sample['filename'], sample['start_line'])
        printDifferentiated('Sample code snippet:', sample['snippet_lines'])

        if sample['documentation'] and raw_input('Sample already has documentation. Overwrite? (y/n)') != 'y':
            continue

        module_name  = sample['filename'].replace('.py', '').replace('/', '.')
        exec('import %s as docsource' % module_name)

        identifier_list = raw_input('Enter a comma separated list of identifiers: ').replace(' ', '').split(',')
        for identifier in identifier_list:
            print 'Searching for docs for %s' % identifier

            docs = ''
            try:
                docs = eval('docsource.%s.__doc__' % identifier)
            except:
                pass

            print 'Found docs:\n%s' % docs
            overwrite = raw_input('Enter different docs to overwrite, or nothing to accept: ')

            if overwrite:
                docs = overwrite
            if docs and docs != 'None':
                sample['documentation'][identifier] = docs

        print 'Writing to file'
        with open(output_file, 'w') as f:
            f.write(json.dumps(project_data))
            print 'json dumped to file'


if __name__ == '__main__':
    main()
