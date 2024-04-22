import unittest
import coverage
import os

def run_tests_with_coverage():
    cov = coverage.Coverage()
    cov.start()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(current_dir, 'tests')

    if not os.path.exists(tests_dir):
        print(f"Directory '{tests_dir}' does not exist.")
        return

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(tests_dir, pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    cov.stop()
    cov.report()

if __name__ == "__main__":
    run_tests_with_coverage()
