"""
Classes for determining risk associated with age of PR
"""
from base import Rule, Category

class TotalAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent commit.
    """
    def __init__(self, pr):
        super(TotalAgeRule, self).__init__(pr)
        self.name = "Total PR Age"
        self.description = "How long has the pull request been open?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        # TODO
        DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        created_date_unicode = self.pr.get('created_at', None)
        created_date = datetime.datetime.strptime(created_date_unicode, DATETIME_FORMAT)
        now = datetime.datetime.now()
        age = (now - created_date).days

        #return age
        return 8

    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        # TODO
        return 1

class LastCommitAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent comment.
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

        # Last commit follows a uri like this: https://api.github.com/repos/edx/configuration/commits/0a038c03e842c3d25d29cb2218c5dfbbaf310130
        # 0a038c03e842c3d25d29cb2218c5dfbbaf310130

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
        super(AgeCat, self).__init__(pr)
        self.rules = [
            (50, LastCommitAgeRule(pr)),
            (50, LastCommentAgeRule(pr)),
        ]
