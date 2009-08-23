import os, shutil, sys, unittest

# Look for coverage.py in __file__/lib as well as sys.path
sys.path = [os.path.join(os.path.dirname(__file__), "lib")] + sys.path

import coverage
from inspect import getmembers, ismodule
from django.test.simple import run_tests as django_test_runner
from django.db.models import get_app, get_apps
from django.conf import settings



def get_coverage_modules(app_module):
    """
    Returns a list of modules to report coverage info for, given an
    application module.
    """
    app_path = app_module.__name__.split('.')[:-1]
    coverage_module = __import__('.'.join(app_path), {}, {}, app_path[-1])

    return [coverage_module] + [attr for name, attr in
        getmembers(coverage_module) if ismodule(attr) and name != 'tests']

def test_runner_with_coverage(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    """Custom test runner.  Follows the django.test.simple.run_tests() interface."""
    coverage.use_cache(0) # Do not cache any of the coverage.py stuff
    coverage.start()
    test_results = django_test_runner(test_labels, verbosity, interactive, extra_tests)
    coverage.stop()

    coverage_modules = []
    if test_labels:
        for label in test_labels:
            # Don't report coverage if you're only running a single
            # test case.
            if '.' not in label:
                app = get_app(label)
                coverage_modules.extend(get_coverage_modules(app))
    else:
        for app in get_apps():
            coverage_modules.extend(get_coverage_modules(app))


    if coverage_modules:
        # Print code metrics header
        print ''
        print '----------------------------------------------------------------------'
        print ' Unit Test Code Coverage Results'
        print '----------------------------------------------------------------------'
        coverage.report(coverage_modules, show_missing=1)
        # Print code metrics footer
        print '----------------------------------------------------------------------'
    return test_results

# test_runner_with_coverage()
