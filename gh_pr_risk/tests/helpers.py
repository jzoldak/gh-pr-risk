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

    If that file does not exist then return an empty dict.
    """
    fixture_filepath = os.path.join(os.path.dirname(__file__),
        'fixtures', rel_path, filename)

    if os.path.isfile(fixture_filepath):

        with open(fixture_filepath) as fixture_file:
            contents = fixture_file.read()

        return loads(contents)

    return {}


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
    uri_pattern = '^([^\/]+)\/(.+)$'
    match = re.search(uri_pattern, uri).groups()
    resource = match[0]

    if resource == 'repos':
        # For calls to the repos object, use the rest of the
        # API call for the filename, replacing occurances of
        # '/' with '_' and appending the suffix .json
        fix_file = '{}.json'.format(match[1].replace('/','_'))
        return_value = load_fixture('repos', fix_file)

    elif resource == 'search':
        # With the tests we have right now we only need one search
        # results file so let's not get fancy. We'll just store it
        # in search/results.json
        return_value = load_fixture('search', 'results.json')


    return return_value

