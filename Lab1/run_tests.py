import unittest
import coverage

# Создание объекта coverage
cov = coverage.Coverage()
cov.start()

# Запуск тестов
loader = unittest.TestLoader()
suite = loader.discover(start_dir='tests', pattern='test_*.py')
runner = unittest.TextTestRunner()
runner.run(suite)

# Остановка сбора покрытия кода
cov.stop()
cov.save()

# Генерация отчета о покрытии
cov.report()
cov.html_report(directory='coverage_html')