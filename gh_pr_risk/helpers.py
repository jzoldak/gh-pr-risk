"""
Helper methods
"""
def risk_format(risk):
    return int(risk*100)

def risk_color(risk):
    if risk >= 0.80:
        return 'FF003C'
    elif risk >= 0.60:
        return 'FF8A00'
    elif risk >= 0.40:
        return 'FABE28'
    elif risk >= 0.20:
        return '88C100'
    else:
        return '00C176'

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

    display['risk'] = risk_format(risk.risk)
    display['risk color'] = risk_color(risk.risk)

    for cat in risk.rules:
        display[cat[1].name + ' risk'] = risk_format(cat[1].risk)
        display[cat[1].name + ' color'] = risk_color(cat[1].risk)
        for rule in cat[1].rules:
            display[rule[1].name + ' risk'] = risk_format(rule[1].risk)
            display[rule[1].name + ' color'] = risk_color(rule[1].risk)

    return display
