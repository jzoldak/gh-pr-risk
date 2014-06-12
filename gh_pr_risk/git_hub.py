"""
Objects returned using the GitHub API
"""
class Repo(object):
    """
    A GitHub repository that you are working with
    """
    def __init__(self, github, org, repo_name):

        self.github = github
        self.org = org
        self.repo_name = repo_name
        self.repo = '{}/{}'.format(org, repo_name)

    def __str__(self):
        return(self.repo)

    @property
    def collaborators(self):
        """
        Retrieve the collaborators for this repo
        """
        uri = 'repos/{}/{}/collaborators'.format(self.org, self.repo_name)
        collaborators = self.github.get(uri)
        return collaborators


class IssuesList(object):
    """
    A list of issues from a GitHub repository
    """
    def __init__(self, github, repo, state=None, issue_type=None):

        self.github = github
        self.repo = str(repo)
        self.state = state
        self.issue_type = issue_type

    @property
    def issues(self):
        """
        Retrieve a list of the Issues from GitHub that match
        the query parameters.

        TODO: Note that a maximum of 100 items are returned at
        a time. If you need more than that number, we will
        need to deal with pagination.
        """
        uri = 'search/issues?q=repo:{}+state:{}+type:{}'.format(
            self.repo, self.state, self.issue_type)
        issues = self.github.get(uri)
        return issues


class PullRequest(object):
    """
    A GitHub Pull Request
    """
    def __init__(self, github, repo, number):

        self.github = github
        self.repo = str(repo)
        self.number = number
        self.pr_itself = self.get_pr_itself()
        self.comments = self.get_comments()
        self.statuses = self.get_statuses()


    def get_pr_itself(self):
        """
        Retrieve the Pull Request from GitHub
        """
        uri = 'repos/{}/pulls/{}'.format(
            self.repo, self.number)
        pr = self.github.get(uri)
        return pr

    def get_comments(self):
        """
        A list of comments on the pull request
        Note that these are issue comments,
        not review comments
        """
        uri = 'repos/{}/issues/{}/comments'.format(
            self.repo, self.number)
        comments = self.github.get(uri)
        return comments

    def get_statuses(self):
        """
        A list of this Pull Request's commit statuses,
        which are the statuses of its head branch
        see: https://developer.github.com/v3/repos/statuses/

        Statuses can be:
        Pending,
        Success,
        Error,
        Failure,
        """
        try:
            sha = self.pr_itself['head']['sha']
        except KeyError:
            """
            The required info was not in the return from
            the call for the PR itself.
            Just return an empty list instead.
            """
            return []

        uri = 'repos/{}/statuses/{}'.format(
            self.repo, sha)
        statuses = self.github.get(uri)
        return statuses

    def set_details(self):
        """
        Details for the Pull Request
        """
        pr_itself = self.pr_itself

        details = {}
        user = pr_itself.get('user', None)
        details['login'] = user['login'] if user else None
        details['title'] = pr_itself.get('title', None)

        # if details['login'] in [collab.get('login', None) for collab in self.repo_collab]:
        #     details['collab'] = 'Yes'
        # else:
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

        return details
