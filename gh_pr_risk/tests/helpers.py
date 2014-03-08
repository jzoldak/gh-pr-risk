"""
Test helper methods
"""
import os.path
from json import loads
import re

def load_fixture(filename):
    """
    Return the contents of the file at 'filename'
    which is stored in the 'fixtures' directory.

    If that file does not exist then return an empty dict.
    """
    fixture_filepath = os.path.join(os.path.dirname(__file__),
        'fixtures', filename)

    if os.path.isfile(fixture_filepath):

        with open(fixture_filepath) as fixture_file:
            contents = fixture_file.read()

        return loads(contents)

    # from nose.tools import set_trace; set_trace()
    print fixture_filepath
    return {}


def fixture_stubs(*args, **kwargs):
    """
    Stub for returning the value from an API call
    to GitHub.

    Return the results from a fixture file instead.
    """
    uri = args[0]
    # from nose.tools import set_trace; set_trace()
    print uri
    return_value = []

    # Compute the name of the fixture file to load
    # from the API call to GitHub

    # First strip off the repos/foo/bar piece
    # because that is not in the filename
    # E.g. for repos/foo/bar/issues/123/comments
    # we just want 123/comments
    uri_pattern = '^repos\/[^\/]+\/[^\/]+\/(.+)$'
    resource = re.search(uri_pattern, uri).groups()[0]

    # Replace the / with an _ in the filename and
    # tack on a .json
    fix_file = '{}.json'.format(resource.replace('/','_'))
    return_value = load_fixture(fix_file)

    return return_value
