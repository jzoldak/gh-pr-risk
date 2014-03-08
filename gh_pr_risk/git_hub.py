"""
Classes for GitHub objects
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

        TODO: Note that a maximum of 100 issues are returned at
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
        self.pr_info = self.get_pr_info()
        self.comments = self.get_comments()
        self.statuses = self.get_statuses()


    def __str__(self):
        return(self.number)

    def get_pr_info(self):
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
        """
        uri = 'repos/{}/statuses/{}'.format(
            self.repo, self.pr_info['head']['sha'])
        statuses = self.github.get(uri)
        return statuses
