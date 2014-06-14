import datetime

import unittest
import mock
import gh_pr_risk.age
from mock import patch, MagicMock

from flask.ext.github import GitHub

from helpers import fixture_stubs

from gh_pr_risk.git_hub import Repo, PullRequest, IssuesList
from gh_pr_risk.age import TotalAgeRule, LastCommentAgeRule
from nose.tools import assert_equal

@patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
class TotalAgeRuleTest(unittest.TestCase):

    def setUp(self):
        self.gh = GitHub(MagicMock())
        self.repo = Repo(self.gh, 'foo', 'bar')

        datetime_patcher = mock.patch.object(
            gh_pr_risk.age.datetime, 'datetime',
            mock.Mock(wraps=datetime.datetime)
        )
        mocked_datetime = datetime_patcher.start()
        mocked_datetime.utcnow.return_value = datetime.datetime(2014, 6, 14)
        self.addCleanup(datetime_patcher.stop)

    def test_get_data_total_age(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, 201)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.get_data(), 3)

    def test_calculate_risk_total_age(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, 201)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.risk, 0.3)

    def test_get_data_total_age_merged(self, mock_get):
        merged = True
        pr = PullRequest(self.gh, self.repo, 202)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.get_data(), 2)

    def test_risk_total_age_merged(self, mock_get):
        merged = True
        pr = PullRequest(self.gh, self.repo, 202)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.risk, 0.2)

    def test_risk_total_age_zero(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, 203)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.risk, 0.0)

    def test_risk_total_age_high(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, 204)
        rule = TotalAgeRule(pr, merged)
        assert_equal(rule.risk, 1.0)

@patch('flask.ext.github.GitHub.get', side_effect=fixture_stubs)
class LastCommentRuleTest(unittest.TestCase):

    def setUp(self):
        self.gh = GitHub(MagicMock())
        self.repo = Repo(self.gh, 'foo', 'bar')

        datetime_patcher = mock.patch.object(
            gh_pr_risk.age.datetime, 'datetime',
            mock.Mock(wraps=datetime.datetime)
        )
        mocked_datetime = datetime_patcher.start()
        mocked_datetime.utcnow.return_value = datetime.datetime(2014, 6, 14)
        self.addCleanup(datetime_patcher.stop)

    def test_no_comment(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, "empty")
        rule = LastCommentAgeRule(pr, merged)
        assert_equal(rule.get_data, 100)

    def test_last_comment_date(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, 220)
        rule = LastCommentAgeRule(pr, merged)
        assert_equal(rule.get_data, 2)

    def test_last_comment_risk(self, mock_get):
        merged = False
        pr = PullRequest(self.gh, self.repo, 220)
        rule = LastCommentAgeRule(pr, merged)
        assert_equal(rule.risk, 0.2)
