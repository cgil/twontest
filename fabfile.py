from __future__ import absolute_import
import os
import sys

from fabric.api import local, task
from fabric.colors import green, red
from fabric.context_managers import settings

from twontest.utils.fab_utils import localenv


@task
def clean():
    """Remove all .pyc files."""
    print green('Clean up .pyc files')
    local("find . -name '*.py[co]' -exec rm -f '{}' ';'")


@task
def lint():
    """Check for lints"""
    print green('Checking for lints')
    local("flake8 `find . -name '*.py' -not -path '*env/*'` --ignore=E501,E702,E712 "
          "--exclude='./docs/*'")


@task
def test(args='', environment='test'):
    """Run tests."""
    os.environ['CONFIG'] = './twontest/tests/test.yaml'
    clean()
    lint()
    print green('Running all tests')
    cmd = ('nosetests -d --verbosity 3 --with-id --nocapture %s' % args)

    with settings(warn_only=True, quiet=True):
        success = local(cmd).succeeded

    if success:
        print(green("Tests finished running with success."))
    else:
        print(red("Test finished running with errors."))
        sys.exit(1)


@task
def shell(environment='development'):
    """Run the shell in the environment."""
    os.environ['CONFIG'] = './config/%s.yaml' % environment
    local("ipython --ipython-dir ./config/")  # useful if ipython is installed


@task
def serve(environment='development'):
    """Start the server."""
    localenv('env DEV=yes python runserver.py', environment=environment)


@task
def bootstrap():
    """Bootstrap the environment."""
    local("mkdir -p logs")
    print green("\nInstalling requirements")
    local("pip install -r requirements-test.txt")
    local("pip install -r requirements.txt")
    local("python setup.py develop")
