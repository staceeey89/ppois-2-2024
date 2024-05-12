import unittest
import coverage

def run_tests_with_coverage():
    # Initialize coverage
    cov = coverage.Coverage()
    cov.start()

    # Discover and run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('../pythonProject', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    # Stop coverage and generate report
    cov.stop()
    cov.report()

if __name__ == "__main__":
    run_tests_with_coverage()
