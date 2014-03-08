import unittest

from mock import MagicMock, patch
from flask.ext.github import GitHub

from gh_pr_risk.git_hub import Repo, PullRequest
from gh_pr_risk.risk import MergeRisk

from helpers import fixture_stubs
from nose.tools import assert_equal


class RepoTest(unittest.TestCase):

    @patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
    def test_collaborators(self, mock_get):
        gh = GitHub(MagicMock())
        collab = Repo(gh, 'foo', 'bar').collaborators
        assert_equal(len(collab), 2)
        assert_equal(collab[0]['login'], 'red')


class PullRequestTest(unittest.TestCase):

    @patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
    def test_comments(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '123')
        assert_equal(len(pr.comments), 3)


class MergeRiskTest(unittest.TestCase):

    @patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
    def test_is_collab(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '124')
        mr = MergeRisk(pr, repo.collaborators)

        assert_equal(mr.details['collab'], 'Yes')

    @patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
    def test_is_not_collab(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '125')
        mr = MergeRisk(pr, repo.collaborators)

        assert_equal(mr.details['collab'], 'No')
