# Test the twitter-text-python library for conformance
# https://github.com/BonsaiDen/twitter-text-python

import sys
from test_twitter_regex import pytest_generate_tests


try:
    import ttp
except ImportError, e:
    print >> sys.stderr, 'Unable to load alt implemenatation: %s' % e
    print >> sys.stderr, 'Please run `git submodule update --init`'
    sys.exit(1)


def test_twitter_text_py(description, text, expected):
    result = ttp.Parser().parse(text)
    assert expected == result.urls
