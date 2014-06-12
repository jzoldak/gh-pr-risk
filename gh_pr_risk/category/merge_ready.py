"""
Classes for determining merge readiness
"""
from base import Rule, Category


class ThumbsUpRule(Rule):
    """
    Rule for calculating risk associated with the number
    of thumbs up on a PR.
    """
    def __init__(self, pr):
        super(ThumbsUpRule, self).__init__()
        self.name = "Thumbs Up"
        self.description = (
            "the number of thumbs up in the PR's comments"
        )

    def get_data(self):
        """
        The number of comments with thumbsup in the pull Request

        TODO: only one thumbsup should count per person, and you it should
        not count if you thumbsup your own pull request. Also maybe we should only
        count thumbs from "official reviewers?" e.g. collaborators?
        """
        num_thumbs = 0
        for comment in self.pr.comments:
            if ':+1:' in comment['body']:
                num_thumbs += 1
        return num_thumbs

    def risk(self):
        num_thumbs = self.get_data()
        if num_thumbs >= 2:
            return 0
        elif num_thumbs == 1:
            return 0.5
        else:
            return 1


class LastStateRule(Rule):
    """
    Rule for calculating risk associated with the number
    of thumbs up on a PR.
    """
    def __init__(self, pr):
        super(LastStateRule, self).__init__()
        self.name = "Last State"
        self.description = (
            "the most recent test state of the PR"
        )

    def get_data(self):
        """
        The status of the last commit from the PR
        """
        if len(self.pr.statuses) > 0:
            return self.pr.statuses[0]['state']
        else:
            return None

    def risk(self):
        data = self.get_data
            
        risk_vals = {
            'success': 0,
            'pending': 0.5,
            'failure': 1,
            'error': 1,
        }

        risk_vals.get(data, None)


class MergeReadyCat(Category):
    def __init__(self, pr):
        super(MergeReadyCat, self).__init__()
        self.rules = [
            (50, ThumbsUpRule(self.pr)),
            (50, LastStateRule(self.pr)),
        ]
