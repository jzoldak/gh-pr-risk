"""
Classes for determining risk associated with age of PR
"""
from base import Rule, Category
import datetime

def get_date_from_unicode(unicode_date):
    """
    :param unicode_date: a date in github-formatted unicode
    :return: datetime
    """

    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    date = datetime.datetime.strptime(unicode_date, DATETIME_FORMAT)
    return date

def get_date_to_compare_against(merged, pr):
    if not merged:
        return datetime.datetime.utcnow()
    else:

        merged_date_unicode = pr.pr_itself.get('merged_at', None)
        return get_date_from_unicode(merged_date_unicode)

class TotalAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent commit.
    """
    def __init__(self, pr, merged):
        super(TotalAgeRule, self).__init__(pr, merged)
        self.name = "Total PR Age"
        self.description = "How long has the pull request been open?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        created_date_unicode = self.pr.pr_itself.get('created_at', None)
        created_date = get_date_from_unicode(created_date_unicode)
        compare_date = get_date_to_compare_against(self.merged, self.pr)
        age = (compare_date - created_date).days

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
            risk = round((0.1 * data), 5)


        return risk

class LastCommentAgeRule(Rule):
    """
    Rule for calculating risk associated the age of
    the most recent comment.
    """
    def __init__(self, pr, merged):
        super(LastCommentAgeRule, self).__init__(pr, merged)
        self.name = "Last Comment Age"
        self.description = "How long ago was the last comment made?"

    @property
    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """

        if len(self.pr.comments) > 0:
            last_commit_date_unicode = self.pr.comments[-1]['updated_at']
        else:
            # Consider no comments on a PR to be bad and assign a high number
            return 100

        last_commit_date = get_date_from_unicode(last_commit_date_unicode)
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
            risk = round((0.1 * data), 5)

        return risk


class AgeCat(Category):
    def __init__(self, pr, merged):
        super(AgeCat, self).__init__(pr, merged)
        self.name = "Age Cat"
        self.rules = [
            (0.80, LastCommentAgeRule(pr, merged)),
            (0.20, TotalAgeRule(pr, merged)),
        ]
