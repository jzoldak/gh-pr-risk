import unittest

from gh_pr_risk.diff_reporter import GitDiffReporter
from gh_pr_risk.diff import GitHubDiffParser

from helpers import load_fixture
from nose.tools import assert_equal, assert_in, assert_true, assert_false
from nose.tools import set_trace


class DiffReporterTest(unittest.TestCase):

    def test_reporter_empty_diff(self):
        dr = GitDiffReporter(diff='')
        assert_equal(len(dr.src_paths_changed()), 0)

    def test_reporter_gh_diff(self):
        diff = load_fixture('diff', 'reporter.diff')
        dr = GitDiffReporter(diff=diff)
        assert_equal(len(dr.src_paths_changed()), 41)
        assert_in('cms/djangoapps/contentstore/tests/test_import.py',
            dr.src_paths_changed())


class DiffParserTest(unittest.TestCase):

    def test_get_changed_files(self):
        diff = load_fixture('diff', 'parser.diff')

        parser = GitHubDiffParser(diff=diff)
        changed_files = parser.get_changed_files()
        assert_equal(len(changed_files), 41)

    def test_only_doc_files(self):
        diff = load_fixture('diff', 'doc_only.diff')

        parser = GitHubDiffParser(diff=diff)
        assert_true(parser.is_only_doc_files)

    def test_not_only_doc_files(self):
        diff = load_fixture('diff', 'parser.diff')

        parser = GitHubDiffParser(diff=diff)
        assert_false(parser.is_only_doc_files)
