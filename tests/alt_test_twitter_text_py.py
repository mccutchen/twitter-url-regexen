# Tests the twitter-text-py library for conformance
# https://github.com/dryan/twitter-text-py

import sys
from test_twitter_regex import pytest_generate_tests


try:
    import twitter_text
except ImportError, e:
    print >> sys.stderr, 'Unable to load alt implemenatation: %s' % e
    print >> sys.stderr, 'Please run `git submodule update --init`'
    sys.exit(1)


def test_twitter_text_py(description, text, expected):
    results = twitter_text.extractor.Extractor(text).extract_urls()
    assert expected == results
