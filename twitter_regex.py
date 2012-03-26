# encoding: utf-8

# A collection of regular expressions for parsing Tweet text. The regular
# expression list is frozen at load time to ensure immutability. These reular
# expressions are used throughout the <tt>Twitter</tt> classes. Special care
# has been taken to make sure these reular expressions work with Tweets in all
# languages.

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

# Character not allowed in Tweets
INVALID_CHARACTERS = map(unichr, [
    0xFFFE, 0xFEFF, # BOM
    0xFFFF,         # Special
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E # Directional change
])
REGEXEN['invalid_control_characters'] = u'[%(INVALID_CHARACTERS)s]' % locals()

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
REGEXEN['latin_accents'] = u'[%(LATIN_ACCENTS)s]' % locals()

PUNCTUATION_CHARS = """!"#$%&'()*+,-./:;<=>?@\[\]^_`{|}~"""
CTRL_CHARS = u"\x00-\x1F\x7F"

# URL related hash regex collection
REGEXEN['valid_preceding_chars'] = u"(?:[^-/\"'!=A-Z0-9_@＠$#＃\\." + u''.join(INVALID_CHARACTERS) + u']|^)'

DOMAIN_VALID_CHARS = u'[^\s' + PUNCTUATION_CHARS + CTRL_CHARS + u''.join(INVALID_CHARACTERS) + u']'
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
(                                                                           #   $1 total match
    (%(valid_preceding_chars)s)                                             #   $2 Preceeding chracter
    (                                                                       #   $3 URL
        (https?://)?                                                        #   $4 Protocol (optional)
        (%(valid_domain)s)                                                  #   $5 Domain(s)
        (?::(%(valid_port_number)s))?                                       #   $6 Port number (optional)
        (/%(valid_url_path)s*)?                                             #   $7 URL Path and anchor
        (\?%(valid_url_query_chars)s*%(valid_url_query_ending_chars)s)?     #   $8 Query String
    )
)""" % REGEXEN
