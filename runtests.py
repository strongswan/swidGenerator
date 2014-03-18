#!/usr/bin/env python
import sys
import pytest
import coverage

if __name__ == '__main__':

    # Start coverage tracking
    cov = coverage.coverage()
    cov.start()

    # Run pytest
    if len(sys.argv) > 1:
        code = pytest.main(sys.argv)
    else:
        code = pytest.main(['tests'])

    # Show coverage report
    cov.stop()
    cov.save()
    cov.report()

    sys.exit(code)
