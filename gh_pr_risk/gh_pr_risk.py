"""
Show GitHub PRs and their calculated merge risk
"""
import os
import logging

from flask import Flask, request, session, g, redirect, url_for
from flask import render_template, render_template_string
from flask_bootstrap import Bootstrap

from flask.ext.github import GitHub

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from git_hub import Repo, IssuesList, PullRequest
from helpers import format_pr_for_display
from global_risk import GlobalRisk

DATABASE_URI = 'sqlite:////tmp/github-flask.db'
DEBUG = True
SECRET_KEY='edx'

# Set these values
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '0fa51816cb65a57549f1')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '156f255fadfd1b2a9bcbcd426e545aa3495002bd')
GITHUB_CALLBACK_URL = os.environ.get('GITHUB_CALLBACK_URL',
    'http://localhost:5000/github-callback')

ORG = os.environ.get('RISK_ORG', 'edx')
REPO_NAME = os.environ.get('RISK_REPO', 'configuration')

# create the application
app = Flask(__name__)
app.config.from_object(__name__)

# setup github-flask for authentication
github = GitHub(app)

# setup sqlalchemy
engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initialize the database
    """
    Base.metadata.create_all(bind=engine)


class User(Base):
    """
    The user table for keeping session and token info
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    github_access_token = Column(Integer)

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response


@app.route('/')
def index():
    return render_template('index.html', user=g.user, org=ORG, repo=REPO_NAME)


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)
    user.github_access_token = access_token
    db_session.commit()

    session['user_id'] = user.id
    return redirect(url_for('index'))


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/prs')
def prs():
    open_prs = []

    repo = Repo(github, ORG, REPO_NAME)

    issues = IssuesList(github, repo, state='open', issue_type='pr').issues
    pr_numbers = [issue['number'] for issue in issues['items']]

    for number in pr_numbers:
        pr = PullRequest(github, repo, number)
        risk = GlobalRisk(pr)
        display = format_pr_for_display(pr, risk)
        open_prs.append(display)

    return render_template('show_prs.html', prs=open_prs, org=ORG, repo=REPO_NAME)

@app.route('/merged')
def merged():
    merged_prs = []

    repo = Repo(github, ORG, REPO_NAME)

    issues = IssuesList(github, repo, state='merged', issue_type='pr').issues
    pr_numbers = [issue['number'] for issue in issues['items']]

    for number in pr_numbers:
        pr = PullRequest(github, repo, number)
        risk = GlobalRisk(pr, merged=True)
        display = format_pr_for_display(pr, risk)
        merged_prs.append(display)

    return render_template('show_merged_prs.html', prs=merged_prs, org=ORG, repo=REPO_NAME)

if __name__ == '__main__':
    init_db()
    logging.basicConfig(level=logging.DEBUG)
    Bootstrap(app.run(debug=True))
