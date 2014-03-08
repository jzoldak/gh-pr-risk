class MergeRisk(object):
    """
    Calculated risk for merging a Pull Request
    """
    def __init__(self, pr, repo_collab):

        self.info = pr.pr_info
        self.comments = pr.comments
        self.statuses = pr.statuses
        self.repo_collab = repo_collab
        self.details = self.set_details()
        self.display = self.set_display()


    def __str__(self):
        return self.info


    def set_details(self):
        """
        Details for the Pull Request
        """
        info = self.info

        details = {}
        details['login'] = info['user']['login']
        details['title'] = info['title']

        if details['login'] in [collab['login'] for collab in self.repo_collab]:
            details['collab'] = 'Yes'
        else:
            details['collab'] = 'No'

        details['comments'] = info['comments']
        details['review_comments'] = info['review_comments']
        details['commits'] = info['commits']
        details['additions'] = info['additions']
        details['deletions'] = info['deletions']
        details['changed_files'] = info['changed_files']
        details['mergeable'] = info['mergeable']
        details['thumbsups'] = self.get_num_thumbs()
        details['last_state'] = self.get_last_state()

        return details


    def get_num_thumbs(self):
        """
        The number of comments with thumbsup in the pull Request
        """
        num_thumbs = 0
        for comment in self.comments:
            if ':+1:' in comment['body']:
                num_thumbs += 1
        return num_thumbs

    def get_last_state(self):
        """
        The status of the last commit from the PR
        """
        return self.statuses[0]['state']

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
