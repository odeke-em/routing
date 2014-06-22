import unittest

def main():
    tLoader = unittest.TestLoader()
    tests = tLoader.discover('tests')
    tRunner = unittest.runner.TextTestRunner()
    tRunner.run(tests)

if __name__ == '__main__':
    main()
