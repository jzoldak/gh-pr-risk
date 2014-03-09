"""
Helper methods for tests
"""
import os.path
from json import loads
import re


def load_fixture(rel_path, filename):
    """
    Return the contents of the file at the relative path and filename
    under the 'fixtures' directory.

    If that file does not exist then return an empty dict or string,
    depending on the extension of the target file.
    """
    fixture_filepath = os.path.join(os.path.dirname(__file__),
        'fixtures', rel_path, filename)

    _, extension = os.path.splitext(filename)

    # Check that the file exists
    if os.path.isfile(fixture_filepath):

        with open(fixture_filepath) as fixture_file:
            contents = fixture_file.read()

        # For a json file we are expecting a dict
        # Otherwise return a string
        if extension == '.json':
            return loads(contents)
        else:
            return contents

    else:
        print 'Warning: Fixture file not found - {}'.format(fixture_filepath)

    # For a json file return an empty dict
    # Otherwise return an empty string
    if extension == '.json':
        return {}

    return ''


def fixture_stubs(*args, **kwargs):
    """
    Stub for returning the value from an API call to GitHub.

    Return the results from a fixture file instead.

    Files are stored in subdirectories named by the
    resource from the GitHub API call, e.g. repos or search
    """
    uri = args[0]
    print uri
    return_value = []

    # Compute the name of the fixture file to load
    # from the API call to GitHub

    # First see if you're trying to get a diff file.
    # Those are all stored in the 'diff' folder, so use that as a resource.
    # Also those calls are direct GitHub urls, not retrieved via the API
    # so strip off the https://github.com/ portion of the uri
    if uri.endswith('.diff'):
        resource = 'diff'
        filename_source = uri.replace('https://github.com/','')
        extension = ''
    else:
        # For other calls, do no use the resource in the
        # filename, but as the folder name.
        uri_pattern = '^([^\/]+)\/(.+)$'
        resource, filename_source = re.search(uri_pattern, uri).groups()
        extension = '.json'

    if resource in ['diff', 'repos']:
        # Determine the filename by replacing occurances of '/'
        # with '_' and appending the suffix .json
        fix_file = '{}{}'.format(filename_source.replace('/','_'), extension)
        return_value = load_fixture(resource, fix_file)

    elif resource == 'search':
        # With the tests we have right now we only need one search
        # results file so let's not get fancy. We'll just store it
        # in search/results.json
        return_value = load_fixture('search', 'results.json')

    return return_value
