class MergeRisk(object):
    """
    Calculated risk for merging a Pull Request
    """
    def __init__(self, pr):

        self.pr_itself = pr.pr_itself
        self.comments = pr.comments
        self.statuses = pr.statuses
        self.repo_collab = repo_collab
        self.details = self.set_details()
        self.display = self.set_display()


    def set_display(self):
        """
        Create a dict with the information about the PR that
        should be passed in to the template for display.
        """
        show = [
            'last_state',
            'mergeable',
            'thumbsups',
            'login',
            'commits',
            'changed_files',
            'title'
        ]
        display = {}
        for key in show:
            display[key] = self.details[key]
        return display
