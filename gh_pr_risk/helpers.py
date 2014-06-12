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

    for cat in risk.rules:
        display[cat[1].name + ' risk'] = cat[1].risk
        for rule in cat[1].rules:
            display[rule[1].name + ' risk'] = rule[1].risk

    return display
