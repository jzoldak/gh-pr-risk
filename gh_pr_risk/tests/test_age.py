import unittest

from mock import Mock, patch, MagicMock
from flask.ext.github import GitHub

from helpers import fixture_stubs

from gh_pr_risk.git_hub import Repo, PullRequest, IssuesList

from gh_pr_risk.age import TotalAgeRule, LastCommentAgeRule
from nose.tools import assert_equal

@patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
class TotalAgeRuleTest(unittest.TestCase):

    def test_get_data(self, mock_get):
        merged = False
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, 201)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.get_data(), 3)

    def test_calculate_risk(self, mock_get):
        merged = False
        gh = GitHub(MagicMock())
        repo = Repo(gh, 'foo', 'bar')
        pr = PullRequest(gh, repo, 201)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.risk, 0.3)
