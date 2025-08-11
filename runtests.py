import sys
import os


import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Ensure the project root (contains the `test` package) is on sys.path first
    project_root = os.path.dirname(__file__)
    sys.path.insert(0, project_root)
    # Optionally add the test directory to help direct discovery/imports
    test_dir = os.path.join(project_root, "test")
    if test_dir not in sys.path:
        sys.path.insert(1, test_dir)

    # Set DJANGO_SETTINGS_MODULE to the settings module inside the test package
    # Use top-level module name to avoid colliding with Python's stdlib "test" package on 3.13+
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    # Initialise Django before discovering/importing tests that touch models
    django.setup()

    # Run tests using Django's test runner (isolated test DB)
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests([test_dir])

    # Run coverage report if coverage is installed and tests were run under coverage
    try:
        import coverage

        cov = coverage.Coverage.current()
        if cov:
            cov.stop()
            cov.save()
            cov.report()
    except Exception:
        pass

    sys.exit(bool(failures))
