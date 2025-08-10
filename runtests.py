import sys
import os
 

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Ensure the test directory is in sys.path
    test_dir = os.path.join(os.path.dirname(__file__), "test")
    sys.path.insert(0, test_dir)

    # Set DJANGO_SETTINGS_MODULE so Django knows where to find settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test.settings")

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
