import re
import yaml
import twitter_regex

url_test_path = 'tests/twitter-text-conformance/extract.yml'
try:
    url_tests = yaml.load(open(url_test_path))['tests']['urls']
except IOError, e:
    import sys
    print >> sys.stderr, 'Conformance tests not found: %s' % e
    print >> sys.stderr, 'Please run `git submodule update --init`'
    sys.exit(1)

def pytest_generate_tests(metafunc):
    for spec in url_tests:
        metafunc.addcall(spec)

def test_url_extraction(description, text, expected):
    matches = re.findall(twitter_regex.REGEXEN['valid_url'], text)
    results = [match[2] for match in matches if match]
    assert expected == results
