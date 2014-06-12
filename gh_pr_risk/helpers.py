"""
Helper methods
"""
def format_pr_for_display(pr):
    """
    Input:
        PullRequest object

    Output:
        Dict with the information about the PR that
        should be passed to the template for display.
    """
    self.pr_itself = pr.pr_itself
    self.comments = pr.comments
    self.statuses = pr.statuses
    self.details = self.set_details()
    self.display = self.set_display()

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
