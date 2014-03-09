from diff import GitHubDiffParser

class MergeRisk(object):
    """
    Calculated risk for merging a Pull Request
    """
    def __init__(self, pr, repo_collab):

        self.pr_itself = pr.pr_itself
        self.comments = pr.comments
        self.statuses = pr.statuses
        self.diff = pr.diff
        self.repo_collab = repo_collab
        self.details = self.set_details()
        self.display = self.set_display()


    def set_details(self):
        """
        Details for the Pull Request
        """
        pr_itself = self.pr_itself

        details = {}
        user = pr_itself.get('user', None)
        details['login'] = user['login'] if user else None
        details['title'] = pr_itself.get('title', None)

        if details['login'] in [collab.get('login', None) for collab in self.repo_collab]:
            details['collab'] = 'Yes'
        else:
            details['collab'] = 'No'

        details['comments'] = pr_itself.get('comments', None)
        details['review_comments'] = pr_itself.get('review_comments', None)
        details['commits'] = pr_itself.get('commits', None)
        details['additions'] = pr_itself.get('additions', None)
        details['deletions'] = pr_itself.get('deletions', None)
        details['changed_files'] = pr_itself.get('changed_files', None)
        details['mergeable'] = pr_itself.get('mergeable', None)
        details['thumbsups'] = self.get_num_thumbs()
        details['last_state'] = self.get_last_state()
        details['doc_only'] = self.only_doc_changes()

        return details


    def get_num_thumbs(self):
        """
        The number of comments with thumbsup in the pull Request

        TODO: only one thumbsup should count per person, and you it should
        not count if you thumbsup your own pull request. Also maybe we should only
        count thumbs from "official reviewers?" e.g. collaborators?
        """
        num_thumbs = 0
        for comment in self.comments:
            if ':+1:' in comment.get('body', []):
                num_thumbs += 1
        return num_thumbs


    def get_last_state(self):
        """
        The status of the last commit from the PR
        """
        if len(self.statuses) > 0:
            return self.statuses[0]['state']
        else:
            return None

    def only_doc_changes(self):
        """
        Whether the only changes in this PR are to doc files.
        """
        return GitHubDiffParser(diff=self.diff).is_only_doc_files

    def set_display(self):
        """
        Create a dict with the information about the PR that
        should be passed in to the template for display.
        """
        show = [
            'last_state',
            'mergeable',
            'thumbsups',
            'doc_only',
            'login',
            'commits',
            'changed_files',
            'title'
        ]
        display = {}
        for key in show:
            display[key] = self.details[key]
        return display
