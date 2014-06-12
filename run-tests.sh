#!/usr/bin/env bash

set -e
nosetests --with-coverage --cover-erase --cover-package=gh_pr_risk,gh_pr_risk.base,gh_pr_risk.git_hub,gh_pr_risk.risk
