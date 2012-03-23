# Twitter URL Regexen

This is an attempt to extract the URL-matching regular expression(s) from the
`twitter-text-rb`[1] project and port them to Python.

## What? Why?

This is important because any service that will be creating tweets on behalf
of its users needs to be able to provide those users an accurate character
count. Should be easy, right?  Nope! Now that Twitter is wrapping URLs in t.co
short links, the service in question will need to know exactly what parts of a
user's tweet will be replaced by shortened t.co URLs.

This is mind-bendingly stupid.

To alleviate some of the pain, Twitter has kindly provided reference
implementations for this behavior for Ruby[1], JavaScript[2], and Java[3],
along with a suite of conformance tests[4] for third party implementers.

Unfortunately, they do not provide and maintain a reference implementation for
Python, and those that exist are incomplete (this particular little lib very
much included).

## Okay, so what is this then?

This project, `twitter-url-regexen`, is just an attempt to extract the
URL-related regular expressions from the `twitter-text-rb` source code
(specifically, [lib/regex.rb][5]) and port them to Python.  Nothing more,
nothing less.

## How good is this port?

Well, it passes 62 of the 70 (at time of writing) URL-extraction conformance
tests. Hopefully, that's good enough for government work (as they say).

## What about those 8 failing tests?

See, here's where things get even dumber. Twitter is not just extracting these
URLs based on a regular expression. There is also a fair amount of extra work
done to, e.g., specially handle t.co URLs, protocol-less ccTLD URLs, non-ASCII
URLs, etc.

This library does not attempt to duplicate that logic, so some of the failures
stem from that basic incompatibility.

Fuck if I know about the other ones.

## See Also

Twitter's own docs about this inane misfeature:
https://dev.twitter.com/docs/tco-url-wrapper/how-twitter-wrap-urls


[1] https://github.com/twitter/twitter-text-rb
[2] https://github.com/twitter/twitter-text-js
[3] https://github.com/twitter/twitter-text-java
[4] https://github.com/twitter/twitter-text-conformance
[5] https://github.com/twitter/twitter-text-rb/blob/master/lib/regex.rb
