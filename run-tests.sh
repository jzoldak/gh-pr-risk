#!/usr/bin/env bash

set -e
nosetests --with-coverage --cover-erase --cover-package=gh-pr-risk
