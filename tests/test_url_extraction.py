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

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
alt_impl_root = os.path.join(root, 'alt_impls')
for alt_impl in os.listdir(alt_impl_root):
    sys.path.insert(0, os.path.join(alt_impl_root, alt_impl))
try:
    import twitter_text
    import ttp
except ImportError, e:
    print >> sys.stderr, 'Unable to load alt implemenatation: %s' % e
    print >> sys.stderr, 'Please run `git submodule update --init`'
    sys.exit(1)

def pytest_generate_tests(metafunc):
    for spec in url_tests:
        metafunc.addcall(spec)

def test_url_extraction(description, text, expected):
    matches = re.findall(twitter_regex.REGEXEN['valid_url'], text)
    results = [match[2] for match in matches if match]
    assert expected == results

def test_twitter_text_py(description, text, expected):
    results = twitter_text.extractor.Extractor(text).extract_urls()
    assert expected == results

def test_twitter_text_python(description, text, expected):
    result = ttp.Parser().parse(text)
    assert expected == result.urls