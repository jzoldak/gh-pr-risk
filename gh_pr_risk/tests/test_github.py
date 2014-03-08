import unittest
from json import loads

from mock import MagicMock, patch
from flask.ext.github import GitHub

from gh_pr_risk.git_hub import Repo

from helpers import load_fixture
from nose.tools import assert_equal


class RepoTest(unittest.TestCase):

    @patch('flask.ext.github.GitHub.get')
    def test_collaborators(self, mock_get):
        mock_get.return_value = loads(load_fixture('collaborators.json'))
        gh = GitHub(MagicMock())
        collab = Repo(gh, 'foo', 'bar').collaborators
        assert_equal(collab[0]['login'], 'red')

