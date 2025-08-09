import sys
import os
import unittest

if __name__ == "__main__":
    # Ensure the test directory is in sys.path
    test_dir = os.path.join(os.path.dirname(__file__), "test")
    sys.path.insert(0, test_dir)

    # Set DJANGO_SETTINGS_MODULE so Django knows where to find settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test.settings")

    # Discover and run tests in the 'test' directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
