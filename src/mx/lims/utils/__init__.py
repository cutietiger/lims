from Products.CMFPlone.utils import safe_unicode
from zope.i18n import translate
import types

def to_utf8(text):
    if text is None:
        text = ''
    return safe_unicode(text).encode('utf-8')

def to_unicode(text):
    if text is None:
        text = ''
    return safe_unicode(text)

def t(i18n_msg):
    """Safely translate and convert to UTF8, any zope i18n msgid returned from
    a _
    """
    return to_utf8(translate(to_unicode(i18n_msg)))

def getFromString(obj, string):
    attrobj = obj
    attrs = string.split('.')
    for attr in attrs:
        if hasattr(attrobj, attr):
            attrobj = getattr(attrobj, attr)
            if isinstance(attrobj, types.MethodType) \
               and callable(attrobj):
                attrobj = attrobj()
        else:
            attrobj = None
            break
    return attrobj if attrobj else None
