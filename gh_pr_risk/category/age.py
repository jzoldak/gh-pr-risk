"""
Classes for determining risk associated with age of PR
"""
from ..base import Rule, Category

class LastCommitAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent commit.
    """
    def __init__(self, pr):
        super(LastCommitAgeRule, self).__init__(pr)
        self.name = "Last Commit Age"
        self.description = "How long ago was the most recent commit made?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        # TODO
        return None

    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        # TODO
        return 1

class LastCommentAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent comment.
    """
    def __init__(self, pr):
        super(LastCommentAgeRule, self).__init__(pr)
        self.name = "Last Comment Age"
        self.description = "How long ago was the most recent comment made?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        # TODO
        return None

    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        # TODO
        return 1


class AgeCat(Category):
    def __init__(self, pr):
        super(Age, self).__init__(pr)
        self.rules = [
            (50, LastCommitAgeRule(self.pr)),
            (50, LastCommentAgeRule(self.pr)),
        ]
