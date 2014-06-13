"""
Base class for a risk feature rule. 
"""

class Category(object):
    """
    Category of features for risk assessment.
    """
    def __init__(self, pr):
        super(Category, self).__init__()
        # A list of tuples such that rule[0] is the rule's weight
        # and rule[1] is the Rule object
        self.rules = []
        self.name = ""

    @property
    def risk(self):
        """
        Returns the sum of the (rule_weight * rule_risk) for self.rules.
        """
        risk = sum([(r[0] * r[1].risk) for r in self.rules])
        return risk
        

class Rule(object):
    """
    Rule for getting data and assessing the risk of
    a feature.
    """
    def __init__(self, pr):
        self.pr = pr
        self.name = ""
        self.description = ""

    def get_data(self):
        """
        Method for obtaining data from github for self.pr.
        """
        return None
    
    @property
    def risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        return None 
