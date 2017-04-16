from zc.relation.interfaces import ICatalog
from zope.component import getUtility, queryUtility
from zope.intid.interfaces import IIntIds
from plone.app.linkintegrity.handlers import referencedRelationship
from zope.interface import implementer
from .interfaces import IMethodRelations,IInstrumentRelations

def get_links(obj,attribute=None, backrefs=False):
    links = []
    for rel in get_relations(obj,attribute=attribute,backrefs=backrefs):
        if not rel.isBroken():
            if backrefs:
                obj = rel.from_object
            else:
                obj = rel.to_object
            links.append(dict(href=obj.absolute_url(),
                                  title=obj.title))
    return links

def get_backlinks(obj,attribute=None):
    backlinks = []
    for rel in get_backrelations(obj,attribute=attribute):
        if not rel.isBroken():
            obj = rel.from_object
            backlinks.append(dict(href=obj.absolute_url(),
                                  title=obj.title))
    return backlinks

def get_relations(obj, attribute=None, backrefs=False):
    """Get any kind of references and backreferences"""
    int_id = get_intid(obj)
    if not int_id:
        return []

    relation_catalog = getUtility(ICatalog)
    if not relation_catalog:
        return []

    query = {}
    if attribute:
        # Constrain the search for certain relation-types.
        query['from_attribute'] = attribute

    if backrefs:
        query['to_id'] = int_id
    else:
        query['from_id'] = int_id

    return relation_catalog.findRelations(query)

def get_backrelations(obj, attribute=None):
    return get_relations(obj, attribute=attribute, backrefs=True)

def get_intid(obj):
    """Return the intid of an object from the intid-catalog"""
    intids = queryUtility(IIntIds)
    if intids is None:
        return
    # check that the object has an intid, otherwise there's nothing to be done
    try:
        return intids.getId(obj)
    except KeyError:
        # The object has not been added to the ZODB yet
        return

@implementer(IMethodRelations)
class MethodRelations(object):
    def __init__(self, context):
        self.context = context

    def getInstruments(self):
        return get_links(self.context,attribute='Method',backrefs=True)

@implementer(IInstrumentRelations)
class InstrumentRelations(object):
    def __init__(self, context):
        self.context = context

    def getMethods(self):
        return get_links(self.context,attribute='Method')
