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
        super(ThumbsUpRule, self).__init__(pr)
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
        super(LastStateRule, self).__init__(pr)
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

        risk_vals.get(data, 1)


class MergableRule(Rule):
    """
    Rule for calculating risk associated the mergability.
    """
    def __init__(self, pr):
        super(MergableRule, self).__init__(pr)
        self.name = "Mergable"
        self.description = "Are there merge conflicts?"

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        return self.pr.details.get('mergeable', None)

    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        mergeable = self.get_data()
        return 0 if mergeable else 1


class MergeReadyCat(Category):
    def __init__(self, pr):
        super(MergeReadyCat, self).__init__(pr)
        self.rules = [
            (33, ThumbsUpRule(pr)),
            (33, LastStateRule(pr)),
            (34, MergableRule(pr)),
        ]
