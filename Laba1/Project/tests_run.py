import unittest
import coverage

cov=coverage.Coverage()

cov.start()

loader=unittest.TestLoader()
suite=loader.discover(start_dir='tests',pattern='*Test.py')
runner=unittest.TextTestRunner()
runner.run(suite)

cov.stop()
cov.save()

cov.report()
cov.html_report(directory='coverage_html')