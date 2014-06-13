import unittest

from mock import Mock

from gh_pr_risk.base import Rule
from nose.tools import assert_equal


class RuleTest(unittest.TestCase):

    def test_get_data(self):
        pr = Mock()
        rule = Rule(pr, merged=False)
        assert_equal(rule.get_data(), None)


    def test_calculate_risk(self):
        pr = Mock()
        rule = Rule(pr, merged=False)
        assert_equal(rule.risk, None)

