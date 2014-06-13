from merge_ready import MergeReadyCat
from age import AgeCat
from diff_files import DiffFilesCat
from base import Category

class GlobalRisk(Category):
    """
    GlobalRisk for PR
    """
    def __init__(self, pr):
        super(GlobalRisk, self).__init__(pr)

        # A list of tuples such that rule[0] is the category's weight
        # and rule[1] is the Rule object
        self.rules = [
            (0.60, MergeReadyCat(pr)),
            (0.20, AgeCat(pr)),
            (0.20, DiffFilesCat(pr)),
        ]
