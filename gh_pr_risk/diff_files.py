"""
Classes for determining merge readiness
"""
from base import Rule, Category

class FileTypeRule(Rule):
    """
    Rule for calculating risk associated the type of files
    that have been changed.
    """
    def __init__(self, pr, merged):
        super(FileTypeRule, self).__init__(pr, merged)
        self.name = "File Type"
        self.description = "Which type of files have been changed?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        diff_files = self.pr.files
        exts = [f['filename'].split('.')[-1] for f in diff_files]
        return exts

    @property
    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        high_risk = ['py', 'js', 'coffee', 'sh', 'rake', 'conf', 'cfg','rb'] 
        med_risk = ['yml', 'json', 'txt', 'xml'] 
        low_risk = ['html', 'rst', 'css', 'md']

        exts = set(self.get_data())

        if exts.intersection(high_risk):
            return 1.0
        elif exts.intersection(med_risk):
            return 0.5
        elif exts.intersection(med_risk):
            return 0.0
        else:
            return 1.0


class FileCountRule(Rule):
    """
    Rule for calculating risk associated the number of files
    that have been changed.
    """
    def __init__(self, pr, merged):
        super(FileCountRule, self).__init__(pr, merged)
        self.name = "File Count"
        self.description = "How many files have been changed?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        diff_files = self.pr.files
        return len(diff_files)

    @property
    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        count = min(self.get_data(), 20)
        return count/20.0


class DiffFilesCat(Category):
    def __init__(self, pr, merged):
        super(DiffFilesCat, self).__init__(pr, merged)
        self.name = 'Diff Files Cat'
        self.rules = [
            (0.50, FileTypeRule(pr, merged)),
            (0.50, FileCountRule(pr, merged)),
        ]
