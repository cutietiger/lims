from plone import api
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18n.locales import locales
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

@implementer(IVocabularyFactory)
class CurrenciesVocabularyFactory(object):
    def __call__(self, context):
        items = []
        currencies = locales.getLocale('zh','cn').numbers.currencies.values()
        currencies.sort(lambda x,y:cmp(x.displayName, y.displayName))
        for c in currencies:
            items.append(SimpleVocabulary.createTerm(
                c.type, c.type,
                "%s (%s)" % (c.displayName, c.symbol)))
        return SimpleVocabulary(items)
CurrenciesVocabulary = CurrenciesVocabularyFactory()

@implementer(IVocabularyFactory)
class SuppliersVocabularyFactory(object):
    def __call__(self, context):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(portal_type='Supplier')
        items = [SimpleTerm(value=b.UID, title=b.Title) for b in brains]
        return SimpleVocabulary(items)
SuppliersVocabulary = SuppliersVocabularyFactory()
