# encoding: utf-8

# A collection of regular expressions for parsing Tweet text. The regular expression
# list is frozen at load time to ensure immutability. These reular expressions are
# used throughout the <tt>Twitter</tt> classes. Special care has been taken to make
# sure these reular expressions work with Tweets in all languages.

REGEXEN = {}

def safe_unichr(n):
    try:
        return unichr(n)
    except ValueError:
        # Thanks, Stack Overflow! http://stackoverflow.com/a/7107319/151221
        h = hex(n).split('0x')[1].zfill(8)
        return (r'\U' + h).decode('unicode-escape')

def regex_range(fro, to=None):
    if to:
        return u'%s-%s' % (safe_unichr(fro), safe_unichr(to))
    else:
        return safe_unichr(fro)

def flatten(xs):
    result = []
    for x in xs:
        if isinstance(x, list):
            result.extend(flatten(x))
        else:
            result.append(x)
    return result

# Space is more than %20, U+3000 for example is the full-width space used with Kanji. Provide a short-hand
# to access both the list of characters and a pattern suitible for use with String#split
#  Taken from: ActiveSupport::Multibyte::Handlers::UTF8Handler::UNICODE_WHITESPACE
UNICODE_SPACES = [
      range(0x0009, 0x000D+1),  # White_Space # Cc   [5] <control-0009>..<control-000D>
      0x0020,          # White_Space # Zs       SPACE
      0x0085,          # White_Space # Cc       <control-0085>
      0x00A0,          # White_Space # Zs       NO-BREAK SPACE
      0x1680,          # White_Space # Zs       OGHAM SPACE MARK
      0x180E,          # White_Space # Zs       MONGOLIAN VOWEL SEPARATOR
      range(0x2000, 0x200A+1), # White_Space # Zs  [11] EN QUAD..HAIR SPACE
      0x2028,          # White_Space # Zl       LINE SEPARATOR
      0x2029,          # White_Space # Zp       PARAGRAPH SEPARATOR
      0x202F,          # White_Space # Zs       NARROW NO-BREAK SPACE
      0x205F,          # White_Space # Zs       MEDIUM MATHEMATICAL SPACE
      0x3000,          # White_Space # Zs       IDEOGRAPHIC SPACE
]
UNICODE_SPACES = map(unichr, flatten(UNICODE_SPACES))
REGEXEN['spaces'] = u'[%(UNICODE_SPACES)s]' % locals()

# Character not allowed in Tweets
INVALID_CHARACTERS = map(unichr, [
  0xFFFE, 0xFEFF, # BOM
  0xFFFF,         # Special
  0x202A, 0x202B, 0x202C, 0x202D, 0x202E # Directional change
])
REGEXEN['invalid_control_characters'] = u'[%(INVALID_CHARACTERS)s]' % locals()

REGEXEN['list_name'] = u'[a-zA-Z][a-zA-Z0-9_\\-\x80-\xff]{0,24}'

# Latin accented characters
# Excludes 0xd7 from the range (the multiplication sign, confusable with "x").
# Also excludes 0xf7, the division sign
LATIN_ACCENTS = u''.join([
      regex_range(0xc0, 0xd6),
      regex_range(0xd8, 0xf6),
      regex_range(0xf8, 0xff),
      regex_range(0x0100, 0x024f),
      regex_range(0x0253, 0x0254),
      regex_range(0x0256, 0x0257),
      regex_range(0x0259),
      regex_range(0x025b),
      regex_range(0x0263),
      regex_range(0x0268),
      regex_range(0x026f),
      regex_range(0x0272),
      regex_range(0x0289),
      regex_range(0x028b),
      regex_range(0x02bb),
      regex_range(0x1e00, 0x1eff)
])

NON_LATIN_HASHTAG_CHARS = u''.join([
  # Cyrillic (Russian, Ukrainian, etc.)
  regex_range(0x0400, 0x04ff), # Cyrillic
  regex_range(0x0500, 0x0527), # Cyrillic Supplement
  regex_range(0x2de0, 0x2dff), # Cyrillic Extended A
  regex_range(0xa640, 0xa69f), # Cyrillic Extended B
  regex_range(0x0591, 0x05bd), # Hebrew
  regex_range(0x05bf),
  regex_range(0x05c1, 0x05c2),
  regex_range(0x05c4, 0x05c5),
  regex_range(0x05c7),
  regex_range(0x05d0, 0x05ea),
  regex_range(0x05f0, 0x05f2),
  regex_range(0xfb12, 0xfb28), # Hebrew Presentation Forms
  regex_range(0xfb2a, 0xfb36),
  regex_range(0xfb38, 0xfb3c),
  regex_range(0xfb3e),
  regex_range(0xfb40, 0xfb41),
  regex_range(0xfb43, 0xfb44),
  regex_range(0xfb46, 0xfb4f),
  regex_range(0x0610, 0x061a), # Arabic
  regex_range(0x0620, 0x065f),
  regex_range(0x066e, 0x06d3),
  regex_range(0x06d5, 0x06dc),
  regex_range(0x06de, 0x06e8),
  regex_range(0x06ea, 0x06ef),
  regex_range(0x06fa, 0x06fc),
  regex_range(0x06ff),
  regex_range(0x0750, 0x077f), # Arabic Supplement
  regex_range(0x08a0),         # Arabic Extended A
  regex_range(0x08a2, 0x08ac),
  regex_range(0x08e4, 0x08fe),
  regex_range(0xfb50, 0xfbb1), # Arabic Pres. Forms A
  regex_range(0xfbd3, 0xfd3d),
  regex_range(0xfd50, 0xfd8f),
  regex_range(0xfd92, 0xfdc7),
  regex_range(0xfdf0, 0xfdfb),
  regex_range(0xfe70, 0xfe74), # Arabic Pres. Forms B
  regex_range(0xfe76, 0xfefc),
  regex_range(0x200c, 0x200c), # Zero-Width Non-Joiner
  regex_range(0x0e01, 0x0e3a), # Thai
  regex_range(0x0e40, 0x0e4e), # Hangul (Korean)
  regex_range(0x1100, 0x11ff), # Hangul Jamo
  regex_range(0x3130, 0x3185), # Hangul Compatibility Jamo
  regex_range(0xA960, 0xA97F), # Hangul Jamo Extended-A
  regex_range(0xAC00, 0xD7AF), # Hangul Syllables
  regex_range(0xD7B0, 0xD7FF), # Hangul Jamo Extended-B
  regex_range(0xFFA1, 0xFFDC)  # Half-width Hangul
])
REGEXEN['latin_accents'] = u'[%(LATIN_ACCENTS)s]' % locals()

CJ_HASHTAG_CHARACTERS = u''.join([
  regex_range(0x30A1, 0x30FA), regex_range(0x30FC, 0x30FE), # Katakana (full-width)
  regex_range(0xFF66, 0xFF9F), # Katakana (half-width)
  regex_range(0xFF10, 0xFF19), regex_range(0xFF21, 0xFF3A), regex_range(0xFF41, 0xFF5A), # Latin (full-width)
  regex_range(0x3041, 0x3096), regex_range(0x3099, 0x309E), # Hiragana
  regex_range(0x3400, 0x4DBF), # Kanji (CJK Extension A)
  regex_range(0x4E00, 0x9FFF), # Kanji (Unified)
  regex_range(0x20000, 0x2A6DF), # Kanji (CJK Extension B)
  regex_range(0x2A700, 0x2B73F), # Kanji (CJK Extension C)
  regex_range(0x2B740, 0x2B81F), # Kanji (CJK Extension D)
  regex_range(0x2F800, 0x2FA1F), regex_range(0x3005), regex_range(0x303B) # Kanji (CJK supplement)
])

PUNCTUATION_CHARS = """!"#$%&'()*+,-./:;<=>?@\[\]^_`{|}~"""
SPACE_CHARS = u" \t\n\x0B\f\r"
CTRL_CHARS = u"\x00-\x1F\x7F"

# A hashtag must contain latin characters, numbers and underscores, but not all numbers.
HASHTAG_ALPHA = u'[a-z_%(LATIN_ACCENTS)s%(NON_LATIN_HASHTAG_CHARS)s%(CJ_HASHTAG_CHARACTERS)s]' % locals()
HASHTAG_ALPHANUMERIC = u'[a-z0-9_%(LATIN_ACCENTS)s%(NON_LATIN_HASHTAG_CHARS)s%(CJ_HASHTAG_CHARACTERS)s]' % locals()
HASHTAG_BOUNDARY = ur'\A|\z|[^&/a-z0-9_%(LATIN_ACCENTS)s%(NON_LATIN_HASHTAG_CHARS)s%(CJ_HASHTAG_CHARACTERS)s]' % locals()

HASHTAG = ur'(%(HASHTAG_BOUNDARY)s)(#|＃)(%(HASHTAG_ALPHANUMERIC)s*%(HASHTAG_ALPHA)s%(HASHTAG_ALPHANUMERIC)s*)' % locals()

REGEXEN['auto_link_hashtags'] = HASHTAG
# Used in Extractor and Rewriter for final filtering
REGEXEN['end_hashtag_match'] = ur'\A(?:[#＃]|://)'

REGEXEN['at_signs'] = ur'[@＠]'
REGEXEN['extract_mentions'] = ur'(^|[^a-zA-Z0-9_!#$%%&*@＠])%(at_signs)s([a-zA-Z0-9_]{1,20})' % REGEXEN
REGEXEN['extract_mentions_or_lists'] = ur'(^|[^a-zA-Z0-9_!#$%%&*@＠])%(at_signs)s([a-zA-Z0-9_]{1,20})(\/[a-zA-Z][a-zA-Z0-9_\-]{0,24})?' % REGEXEN
REGEXEN['extract_reply'] = u'^(?:%(spaces)s)*%(at_signs)s([a-zA-Z0-9_]{1,20})' % REGEXEN
# Used in Extractor and Rewriter for final filtering
REGEXEN['end_screen_name_match'] = ur'\A(?:%(at_signs)s|%(latin_accents)s|://)' % REGEXEN

REGEXEN['auto_link_usernames_or_lists'] = ur'([^a-zA-Z0-9_!#$%&*@＠]|^|RT:?)([@＠]+)([a-zA-Z0-9_]{1,20})(/[a-zA-Z][a-zA-Z0-9_\-]{0,24})?'
REGEXEN['auto_link_emoticon'] = ur'(8\-\#|8\-E|\+\-\(|\`\@|\`O|\&lt;\|:~\(|\}:o\{|:\-\[|\&gt;o\&lt;|X\-/|\[:-\]\-I\-|////Ö\\\\\\\\|\(\|:\|/\)|∑:\*\)|\( \| \))'

# URL related hash regex collection
REGEXEN['valid_preceding_chars'] = u"(?:[^-/\"'!=A-Z0-9_@＠$#＃\\." + u''.join(INVALID_CHARACTERS) + u']|^)'

DOMAIN_VALID_CHARS = u'[^' + PUNCTUATION_CHARS + SPACE_CHARS + CTRL_CHARS + u''.join(INVALID_CHARACTERS) + u''.join(UNICODE_SPACES) + u']'
REGEXEN['valid_subdomain'] = ur'(?:(?:%(DOMAIN_VALID_CHARS)s(?:[_-]|%(DOMAIN_VALID_CHARS)s)*)?%(DOMAIN_VALID_CHARS)s\.)' % locals()
REGEXEN['valid_domain_name'] = ur'(?:(?:%(DOMAIN_VALID_CHARS)s(?:[-]|%(DOMAIN_VALID_CHARS)s)*)?%(DOMAIN_VALID_CHARS)s\.)' % locals()

REGEXEN['valid_gTLD'] = ur'(?:(?:aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|xxx)(?=[^a-z]|$))'
REGEXEN['valid_ccTLD'] = ur"""
      (?:
        (?:ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|
        ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|
        gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|
        lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|
        pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|ss|st|su|sv|sy|sz|tc|td|tf|tg|th|
        tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw)
        (?=[^a-z]|$)
      )
"""
REGEXEN['valid_punycode'] = ur'(?:xn--[0-9a-z]+)'

REGEXEN['valid_domain'] = ur"""(?:
    %(valid_subdomain)s*%(valid_domain_name)s
    (?:%(valid_gTLD)s|%(valid_ccTLD)s|%(valid_punycode)s)
)""" % REGEXEN

# This is used in Extractor
REGEXEN['valid_ascii_domain'] = ur"""
    (?:(?:[A-Za-z0-9\-_]|%(latin_accents)s)+\.)+
    (?:%(valid_gTLD)s|%(valid_ccTLD)s|%(valid_punycode)s)
""" % REGEXEN

# This is used in Extractor for stricter t.co URL extraction
REGEXEN['valid_tco_url'] = ur'^https?://t\.co/[a-z0-9]+'

# This is used in Extractor to filter out unwanted URLs.
REGEXEN['invalid_short_domain'] = ur'\A%(valid_domain_name)s%(valid_ccTLD)s\Z' % REGEXEN

REGEXEN['valid_port_number'] = ur'[0-9]+'

REGEXEN['valid_general_url_path_chars'] = ur"""[a-z0-9!\*';:=\+\,\.\$/%%#\[\]\-_~&|%(LATIN_ACCENTS)s]""" % locals()
# Allow URL paths to contain balanced parens
#  1. Used in Wikipedia URLs like /Primer_(film)
#  2. Used in IIS sessions like /S(dfd346)/
REGEXEN['valid_url_balanced_parens'] = ur'\(%(valid_general_url_path_chars)s+\)' % REGEXEN
# Valid end-of-path chracters (so /foo. does not gobble the period).
#   1. Allow =&# for empty URL parameters and other URL-join artifacts
REGEXEN['valid_url_path_ending_chars'] = u'[a-z0-9=_#/+\\-' + LATIN_ACCENTS + u']|(?:' + REGEXEN['valid_url_balanced_parens'] + u')'
# Allow @ in a url, but only in the middle. Catch things like http://example.com/@user/
REGEXEN['valid_url_path'] = ur"""(?:
  (?:
    %(valid_general_url_path_chars)s*
    (?:%(valid_url_balanced_parens)s %(valid_general_url_path_chars)s*)*
    %(valid_url_path_ending_chars)s
  )|(?:@%(valid_general_url_path_chars)s+/)
)""" % REGEXEN

REGEXEN['valid_url_query_chars'] = ur"""[a-z0-9!?\*'\(\);:&=\+\$/%#\[\]\-_\.,~|]"""
REGEXEN['valid_url_query_ending_chars'] = ur'[a-z0-9_&=#/]'
REGEXEN['valid_url'] = ur"""(?iux)
  (                                                                     #   $1 total match
    (%(valid_preceding_chars)s)                                         #   $2 Preceeding chracter
    (                                                                   #   $3 URL
      (https?://)?                                                      #   $4 Protocol (optional)
      (%(valid_domain)s)                                                #   $5 Domain(s)
      (?::(%(valid_port_number)s))?                                     #   $6 Port number (optional)
      (/%(valid_url_path)s*)?                                           #   $7 URL Path and anchor
      (\?%(valid_url_query_chars)s*%(valid_url_query_ending_chars)s)?   #   $8 Query String
    )
  )""" % REGEXEN

# These URL validation pattern strings are based on the ABNF from RFC 3986
REGEXEN['validate_url_unreserved'] = ur'[a-z0-9\-._~]'
REGEXEN['validate_url_pct_encoded'] = ur'(?:%[0-9a-f]{2})'
REGEXEN['validate_url_sub_delims'] = ur"""[!$&'()*+,;=]"""
REGEXEN['validate_url_pchar'] = ur"""(?:
  %(validate_url_unreserved)s|
  %(validate_url_pct_encoded)s|
  %(validate_url_sub_delims)s|
  [:\|@]
)""" % REGEXEN

REGEXEN['validate_url_scheme'] = ur'(?:[a-z][a-z0-9+\-.]*)'
REGEXEN['validate_url_userinfo'] = ur"""(?:
  %(validate_url_unreserved)s|
  %(validate_url_pct_encoded)s|
  %(validate_url_sub_delims)s|
  :
)""" % REGEXEN

REGEXEN['validate_url_dec_octet'] = ur'/(?:[0-9]|(?:[1-9][0-9])|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5]))'
REGEXEN['validate_url_ipv4'] = \
  ur'(?:%(validate_url_dec_octet)s(?:\.%(validate_url_dec_octet)s){3})'

# Punting on real IPv6 validation for now
REGEXEN['validate_url_ipv6'] = ur'(?:\[[a-f0-9:\.]+\])'

# Also punting on IPvFuture for now
REGEXEN['validate_url_ip'] = ur"""(?:
  %(validate_url_ipv4)s|
  %(validate_url_ipv6)s
)""" % REGEXEN

# This is more strict than the rfc specifies
REGEXEN['validate_url_subdomain_segment'] = ur'(?:[a-z0-9](?:[a-z0-9_\-]*[a-z0-9])?)'
REGEXEN['validate_url_domain_segment'] = ur'(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?)'
REGEXEN['validate_url_domain_tld'] = ur'(?:[a-z](?:[a-z0-9\-]*[a-z0-9])?)'
REGEXEN['validate_url_domain'] = ur"""(?:(?:%(validate_url_subdomain_segment)s\.)*
                                 (?:%(validate_url_domain_segment)s\.)
                                 %(validate_url_domain_tld)s)""" % REGEXEN

REGEXEN['validate_url_host'] = ur"""(?:
  %(validate_url_ip)s|
  %(validate_url_domain)s
)""" % REGEXEN

# Unencoded internationalized domains - this doesn't check for invalid UTF-8 sequences
REGEXEN['validate_url_unicode_subdomain_segment'] = \
  ur'(?:(?:[a-z0-9]|[^\x00-\x7f])(?:(?:[a-z0-9_\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)'
REGEXEN['validate_url_unicode_domain_segment'] = \
  ur'(?:(?:[a-z0-9]|[^\x00-\x7f])(?:(?:[a-z0-9\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)'
REGEXEN['validate_url_unicode_domain_tld'] = \
  ur'(?:(?:[a-z]|[^\x00-\x7f])(?:(?:[a-z0-9\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)'
REGEXEN['validate_url_unicode_domain'] = ur"""(?:(?:%(validate_url_unicode_subdomain_segment)s\.)*
                                         (?:%(validate_url_unicode_domain_segment)s\.)
                                         %(validate_url_unicode_domain_tld)s)""" % REGEXEN

REGEXEN['validate_url_unicode_host'] = ur"""(?:
  %(validate_url_ip)s|
  %(validate_url_unicode_domain)s
)""" % REGEXEN

REGEXEN['validate_url_port'] = ur'[0-9]{1,5}'

REGEXEN['validate_url_unicode_authority'] = ur"""
  (?:(%(validate_url_userinfo)s)@)?     #  $1 userinfo
  (%(validate_url_unicode_host)s)       #  $2 host
  (?::(%(validate_url_port)s))?         #  $3 port
""" % REGEXEN

REGEXEN['validate_url_authority'] = ur"""
  (?:(%(validate_url_userinfo)s)@)?     #  $1 userinfo
  (%(validate_url_host)s)               #  $2 host
  (?::(%(validate_url_port)s))?         #  $3 port
""" % REGEXEN

REGEXEN['validate_url_path'] = ur'(/%(validate_url_pchar)s*)*' % REGEXEN
REGEXEN['validate_url_query'] = ur'(%(validate_url_pchar)s|/|\?)*' % REGEXEN
REGEXEN['validate_url_fragment'] = ur'(%(validate_url_pchar)s|/|\?)*' % REGEXEN

# Modified version of RFC 3986 Appendix B
REGEXEN['validate_url_unencoded'] = ur"""
  \A                                #  Full URL
  (?:
    ([^:/?#]+)://                  #  $1 Scheme
  )?
  ([^/?#]*)                        #  $2 Authority
  ([^?#]*)                         #  $3 Path
  (?:
    \?([^#]*)                      #  $4 Query
  )?
  (?:
    \#(.*)                         #  $5 Fragment
  )?\Z
""" % REGEXEN
