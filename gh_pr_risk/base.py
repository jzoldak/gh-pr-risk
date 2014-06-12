"""
Base class for a risk feature rule. 
"""

class Rule(object):
    def __init__(self, pr):
        self.pr = pr
        self.name = ""
        self.description = ""

    def get_data(self):
        """
        Method for obtaining data from github for self.pr
        """
        return None

    def calculate_risk(self):
        """
        Uses data returned from self.get_data to calculate
        the risk associated with this feature.
        """
        return None 
