import unittest

from mock import Mock, MagicMock, patch
from flask.ext.github import GitHub

from gh_pr_risk.git_hub import Repo, PullRequest, IssuesList
from gh_pr_risk.risk import MergeRisk

from helpers import fixture_stubs
from nose.tools import assert_equal, assert_in


def diff_get_response(*args):
    """
    Helper for patching calls that use diff fixtures.
    The requests.get method needs to be patched and to return
    a response from the fixture file instead.
    """
    uri = args[0]
    response = Mock()
    response.content = fixture_stubs(uri)
    return response


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

    def test_pr_statuses(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '122')
        assert_equal(len(pr.statuses), 3)
        assert_equal(pr.statuses[0]['state'], 'pending')

    def test_pr_comments(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '123')
        assert_equal(len(pr.comments), 3)

    @patch('requests.get', side_effect=diff_get_response)
    def test_pr_diff(self, mock_get, mock_response):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '129')
        assert_in('diff --git a/README.rst b/README.rst', pr.diff)


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

    def test_no_thumbs(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '124')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['thumbsups'], 0)

    def test_one_thumbs(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '126')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['thumbsups'], 1)

    def test_multiple_thumbs(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '127')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['thumbsups'], 2)

    def test_last_state(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '122')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['last_state'], 'pending')

    def test_no_status(self, mock_get):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '126')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['last_state'], None)

    @patch('requests.get', side_effect=diff_get_response)
    def test_only_doc_changes(self, mock_get, mock_response):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '129')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['doc_only'], True)

    @patch('requests.get', side_effect=diff_get_response)
    def test_not_only_doc_changes(self, mock_get, mock_response):
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, '130')
        mr = MergeRisk(pr, repo.collaborators)
        assert_equal(mr.details['doc_only'], False)
