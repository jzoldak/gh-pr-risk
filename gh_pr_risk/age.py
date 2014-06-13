"""
Classes for determining risk associated with age of PR
"""
from base import Rule, Category
import datetime

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
        DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        created_date_unicode = self.pr.pr_itself.get('created_at', None)
        created_date = datetime.datetime.strptime(created_date_unicode, DATETIME_FORMAT)
        now = datetime.datetime.utcnow()
        age = (now - created_date).days

        #return age
        return age

    @property
    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        data = self.get_data()

        if data in (0, 1):
            risk = 0.0
        elif data > 10:
            risk = 1.0
        else:
            risk = 0.1 * data


        return risk

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

        DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        last_commit_date_unicode = self.pr.commits[-1]['commit']['author']['date']
        last_commit_date = datetime.datetime.strptime(last_commit_date_unicode, DATETIME_FORMAT)
        now = datetime.datetime.utcnow()
        age = (now - last_commit_date).days

        return age


    @property
    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """

        data = self.get_data()

        if data in (0, 1):
            risk = 0.0
        elif data > 10:
            risk = 1.0
        else:
            risk = 0.1 * data

        return risk


class AgeCat(Category):
    def __init__(self, pr):
        super(AgeCat, self).__init__(pr)
        self.name = "Age Cat"
        self.rules = [
            (0.80, LastCommitAgeRule(pr)),
            (0.20, TotalAgeRule(pr)),
        ]
