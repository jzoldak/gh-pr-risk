"""
Classes for calculations from the GitHub diff
"""
from diff_reporter import GitDiffReporter
import os.path

FILE_TYPES_BY_EXT = {
    'doc': ['.md', '.rst'],
}


class GitHubDiffParser(object):
    """
    Parse the GitHub diff and return interesting results
    """
    def __init__(self, diff=''):
        self.reporter = GitDiffReporter(diff=diff)

    def _get_file_exts(self):
        """
        Return the unique set of file extensions from
        the changed files
        """
        exts = set()
        for filepath in self.get_changed_files():
            _, extension = os.path.splitext(filepath)
            exts.add(extension)

        return exts

    def get_changed_files(self):
        return self.reporter.src_paths_changed()

    @property
    def is_only_doc_files(self):
        changed_exts = self._get_file_exts()
        doc_set = set(FILE_TYPES_BY_EXT['doc'])

        # If the changed extensions is the empty set then something
        # went wrong retrieving the diff, so do not report that
        # the changes are doc only.
        return len(changed_exts) > 0 and changed_exts.issubset(doc_set)
