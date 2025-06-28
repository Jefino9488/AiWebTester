#!/usr/bin/env python
import argparse
import pytest
import sys
import json
from pathlib import Path


def load_config():
    """Load the test configuration file."""
    config_path = Path(__file__).parent / 'tests' / 'config.json'
    with open(config_path) as f:
        return json.load(f)


def update_config(browser=None, headless=None):
    """Update the configuration file with command line arguments."""
    config = load_config()
    if browser:
        config['webdriver']['browser'] = browser
    if headless is not None:
        config['webdriver']['headless'] = headless

    config_path = Path(__file__).parent / 'tests' / 'config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='AI Web Testing Framework Runner')
    parser.add_argument('--test-path', '-t',
                       help='Path to test file or directory to run',
                       default='tests')
    parser.add_argument('--browser', '-b',
                       choices=['chrome', 'firefox', 'edge'],
                       help='Browser to run tests in')
    parser.add_argument('--headless',
                       action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--markers', '-m',
                       help='Only run tests with specified markers (e.g., smoke, regression)')
    parser.add_argument('--parallel', '-n',
                       type=int,
                       help='Number of parallel processes for test execution')
    parser.add_argument('--report',
                       help='Path to save the HTML report',
                       default='report.html')
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')

    args = parser.parse_args()

    # Update configuration if browser or headless mode is specified
    if args.browser or args.headless:
        update_config(args.browser, args.headless)

    # Construct pytest arguments
    pytest_args = [args.test_path]

    if args.markers:
        pytest_args.extend(['-m', args.markers])

    if args.parallel:
        pytest_args.extend(['-n', str(args.parallel)])

    if args.verbose:
        pytest_args.append('-v')

    # Add HTML report generation
    pytest_args.extend(['--html', args.report, '--self-contained-html'])

    # Run pytest with constructed arguments
    return pytest.main(pytest_args)


if __name__ == '__main__':
    sys.exit(main())
