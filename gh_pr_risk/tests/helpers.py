"""
Test helper methods
"""
import os.path

def load_fixture(filename):
    """
    Return the contents of the file at `filename`
    which is stored in the "fixtures" directory.
    """
    fixture_filepath = os.path.join(os.path.dirname(__file__),
        'fixtures', filename)
    with open(fixture_filepath) as fixture_file:
        contents = fixture_file.read()

    return contents
