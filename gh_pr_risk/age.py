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

class LastCommentAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent comment.
    """
    def __init__(self, pr):
        super(LastCommentAgeRule, self).__init__(pr)
        self.name = "Last Comment Age"
        self.description = "How long ago was the last comment made?"

    @property
    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """

        DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        if len(self.pr.comments) > 0:
            last_commit_date_unicode = self.pr.comments[-1]['updated_at']
        else:
            # Consider no comments on a PR to be bad and assign a high number
            return 100
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

        data = self.get_data

        if data in (0, 1):
            risk = 0.0
        elif data > 10:
            risk = 1.0
        else:
            risk = 0.1 * data

        return risk


class AgeCat(Category):
    def __init__(self, pr, merged):
        super(AgeCat, self).__init__(pr, merged)
        self.name = "Age Cat"
        self.rules = [
            (0.80, LastCommentAgeRule(pr)),
            (0.20, TotalAgeRule(pr)),
        ]
