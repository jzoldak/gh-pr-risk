"""
Helper methods
"""
def format_pr_for_display(pr, risk):
    """
    Input:
        PullRequest object

    Output:
        Dict with the information about the PR that
        should be passed to the template for display.
    """
    show = [
        'number',
        'login',
        'title'
    ]
    display = {}
    for key in show:
        display[key] = pr.details[key]

    display['risk'] = risk.risk
    return display
