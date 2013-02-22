import os
import re
import sys
import yaml
import twitter_regex


url_test_path = 'tests/twitter-text-conformance/extract.yml'
try:
    url_tests = yaml.load(open(url_test_path))['tests']['urls']
except IOError, e:
    print >> sys.stderr, 'Conformance tests not found: %s' % e
    print >> sys.stderr, 'Please run `git submodule update --init`'
    sys.exit(1)


# Add alt implementation paths to sys.path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
alt_impl_root = os.path.join(root, 'alt_impls')
for alt_impl in os.listdir(alt_impl_root):
    sys.path.insert(0, os.path.join(alt_impl_root, alt_impl))


def pytest_generate_tests(metafunc):
    for spec in url_tests:
        metafunc.addcall(spec)


def test_twitter_regex(description, text, expected):
    matches = re.findall(twitter_regex.REGEXEN['valid_url'], text)
    results = [match[2] for match in matches if match]
    assert expected == results
