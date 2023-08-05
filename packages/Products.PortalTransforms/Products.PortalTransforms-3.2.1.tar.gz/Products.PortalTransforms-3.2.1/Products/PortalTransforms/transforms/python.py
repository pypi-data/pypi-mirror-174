# -*- coding: utf-8 -*-
"""
Original code from active state recipe
        'Colorize Python source using the built-in tokenizer'

----------------------------------------------------------------------------
     MoinMoin - Python Source Parser

 This code is part of MoinMoin (http://moin.sourceforge.net/) and converts
 Python source code to HTML markup, rendering comments, keywords, operators,
 numeric and string literals in different colors.

 It shows how to use the built-in keyword, token and tokenize modules
 to scan Python source code and re-emit it with no changes to its
 original formatting (which is the hard part).
"""

from DocumentTemplate.html_quote import html_quote
from io import BytesIO
from Products.PortalTransforms.interfaces import ITransform
from Products.PortalTransforms.utils import safe_nativestring
from zope.interface import implementer

import keyword
import six
import token
import tokenize


# Python Source Parser #####################################################

_KEYWORD = token.NT_OFFSET + 1
_TEXT = token.NT_OFFSET + 2


class Parser(object):
    """ Send colored python source.
    """

    def __init__(self, raw, tags):
        """ Store the source text.
        """
        self.raw = raw.expandtabs().strip()
        self.out = BytesIO()
        self.tags = tags

    def __call__(self):
        """ Parse and send the colored source.
        """
        # store line offsets in self.lines
        self.lines = [0, 0]
        pos = 0
        while True:
            pos = self.raw.find(b'\n', pos) + 1
            if not pos:
                break
            self.lines.append(pos)
        self.lines.append(len(self.raw))
        # parse the source and write it
        self.pos = 0
        text = BytesIO(self.raw)
        self.out.write(b'<pre class="python">\n')
        try:
            if six.PY2:
                tokenize.tokenize(text.readline, self.format_tokenizer)
            else:
                for args in tokenize.tokenize(text.readline):
                    self.format_tokenizer(*args)
        except tokenize.TokenError as ex:
            msg = ex.args[0]
            line = ex.args[1][0]
            self.out.write(b"<h5 class='error>'ERROR: %s%s</h5>" % (
                msg, self.raw[self.lines[line]:]))
        self.out.write(b'\n</pre>\n')
        return safe_nativestring(self.out.getvalue())

    def format_tokenizer(self, toktype, toktext, sx, ex, line):
        """ Token handler.
        """
        (srow, scol) = sx
        (erow, ecol) = ex
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)

        # skip encoding
        if six.PY3 and toktype == tokenize.ENCODING:
            return

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            self.out.write(b'\n')
            return

        # send the original whitespace, if needed
        if newpos > oldpos:
            self.out.write(self.raw[oldpos:newpos])

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return

        # map token type to a group
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = 'OP'
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = 'KEYWORD'
        else:
            toktype = tokenize.tok_name[toktype]

        open_tag = self.tags.get('OPEN_' + toktype, self.tags['OPEN_TEXT'])
        close_tag = self.tags.get('CLOSE_' + toktype, self.tags['CLOSE_TEXT'])

        # send text
        self.out.write(open_tag)
        self.out.write(six.b(html_quote(toktext)))
        self.out.write(close_tag)


@implementer(ITransform)
class PythonTransform(object):
    """Colorize Python source files
    """

    __name__ = "python_to_html"
    inputs = ("text/x-python",)
    output = "text/html"

    config = {
        'OPEN_NUMBER': b'<span style="color: #0080C0;">',
        'CLOSE_NUMBER': b'</span>',
        'OPEN_OP': b'<span style="color: #0000C0;">',
        'CLOSE_OP': b'</span>',
        'OPEN_STRING': b'<span style="color: #004080;">',
        'CLOSE_STRING': b'</span>',
        'OPEN_COMMENT': b'<span style="color: #008000;">',
        'CLOSE_COMMENT': b'</span>',
        'OPEN_NAME': b'<span style="color: #000000;">',
        'CLOSE_NAME': b'</span>',
        'OPEN_ERRORTOKEN': b'<span style="color: #FF8080;">',
        'CLOSE_ERRORTOKEN': b'</span>',
        'OPEN_KEYWORD': b'<span style="color: #C00000;">',
        'CLOSE_KEYWORD': b'</span>',
        'OPEN_TEXT': b'',
        'CLOSE_TEXT': b'',
    }

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        if isinstance(orig, six.text_type):
            orig = orig.encode('utf8')
        parser = Parser(orig, self.config)
        data.setData(parser())
        return data


def register():
    return PythonTransform()
