import unittest

from mock import MagicMock, patch
from flask.ext.github import GitHub

from gh_pr_risk.git_hub import Repo, PullRequest, IssuesList
from gh_pr_risk.risk import MergeRisk

from helpers import fixture_stubs
from nose.tools import assert_equal, assert_in


@patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
class GitHubTest(unittest.TestCase):

    def test_repo_collaborators(self, mock_get):
        gh = GitHub(MagicMock())
        collab = Repo(gh, 'foo', 'bar').collaborators
        assert_equal(len(collab), 2)
        assert_equal(collab[0]['login'], 'red')

    def test_issues(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        issues = IssuesList(gh, repo, 'open', 'pr').issues
        assert_in('items', issues)
        assert_equal(len(issues['items']), 3)

    def test_pr_comments(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '123')
        assert_equal(len(pr.comments), 3)

    def test_pr_statuses(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '122')
        assert_equal(len(pr.statuses), 3)
        assert_equal(pr.statuses[0]['state'], 'pending')



@patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
class MergeRiskTest(unittest.TestCase):

    def test_is_collab(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '124')
        mr = MergeRisk(pr, repo.collaborators)

        assert_equal(mr.details['collab'], 'Yes')

    def test_is_not_collab(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '125')
        mr = MergeRisk(pr, repo.collaborators)

        assert_equal(mr.details['collab'], 'No')
