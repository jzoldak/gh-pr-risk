"""
Show GitHub PRs and their calculated merge risk
"""
import os
import logging

from flask import Flask, request, session, g, redirect, url_for
from flask import render_template, render_template_string

from flask.ext.github import GitHub

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from git_hub import Repo, IssuesList, PullRequest
from risk import MergeRisk

DATABASE_URI = 'sqlite:////tmp/github-flask.db'
DEBUG = True
SECRET_KEY='edx'

# Set these values
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', None)
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', None)
GITHUB_CALLBACK_URL = os.environ.get('GITHUB_CALLBACK_URL',
    'http://localhost:5000/github-callback')

ORG = 'edx'
# REPO = 'edx-platform'
REPO_NAME = 'bok-choy'

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
    if g.user:
        t = 'Hello! <a href="{{ url_for("prs") }}">See Pull Requests</a> ' \
            '<a href="{{ url_for("logout") }}">Logout</a>'
    else:
        t = 'Hello! <a href="{{ url_for("login") }}">Login</a>'

    return render_template_string(t)


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
    collaborators = repo.collaborators

    issues = IssuesList(github, repo, 'open', 'pr').issues
    pr_numbers = [issue['number'] for issue in issues['items']]

    for number in pr_numbers:
        pr = PullRequest(github, repo, number)
        display = MergeRisk(pr, collaborators).display
        open_prs.append(display)

    return render_template('show_prs.html', prs=open_prs)


if __name__ == '__main__':
    init_db()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
