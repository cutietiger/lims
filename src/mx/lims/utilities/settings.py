from zope.interface import implementer
from .interfaces import ISettingsProvider,ISettingsFactory
from mx.lims import _

@implementer(ISettingsProvider)
class MethodListSettings(object):
    """
    Table list settings for Methods
    """
    def __init__(self, context):
        self.context = context

    def getColumns(self):
        """ Columns definition """
        return {
            'title': {'title': _('Method'),
                      'index': 'sortable_title',
                      'toggle': False},
            'description': {'title': _('Description'),
                            'toggle': True},
            'instruments': {'title': _('Instruments'),
                            'toggle': True},
            'manual': {'title': _('Manual'),
                                     'toggle': True},
        }

    def getStates(self):
        """ Available review states """
        return [
            {'id':'default',
             'title': self.context.translate(_('Active')),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate', 'title': _('Deactivate')}, ],
             'columns': ['title', 
                         'description',
                         'instruments',
                         'manual']},
            {'id':'inactive',
             'title': self.context.translate(_('Dormant')),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate', 'title': _('Activate')}, ],
             'columns': ['title', 
                         'description',
                         'instruments',
                         'manual']},
            {'id':'all',
             'title': self.context.translate(_('All')),
             'contentFilter':{},
             'columns': ['title', 
                         'description',
                         'instruments',
                         'manual']},
        ]

    def getAjaxUrl(self):
        return '/@@get_methods'

    def getContentFilter(self):
        return {'portal_type': 'Method'}

@implementer(ISettingsFactory)
class MethodListSettingsFactory(object):
    def __call__(self, context):
        return MethodListSettings(context)

@implementer(ISettingsProvider)
class InstrumentListSettings(object):
    """
    Table list settings for Instruments
    """
    def __init__(self, context):
        self.context = context

    def getColumns(self):
        """ Columns definition """
        return {
            'title': {
                'title': _('Method'),
                'index': 'sortable_title',
                'toggle': False},
            'description': {
                'title': _('Description'),
                'toggle': True},
            'methods': {
                'title': _('Methods'),
                'toggle': True},
        }

    def getStates(self):
        """ Available review states """
        return [
            {'id':'default',
             'title': self.context.translate(_('Active')),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate', 'title': _('Deactivate')}, ],
             'columns': ['title', 
                         'description',
                         'methods']},
            {'id':'inactive',
             'title': self.context.translate(_('Dormant')),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate', 'title': _('Activate')}, ],
             'columns': ['title', 
                         'description',
                         'methods']},
            {'id':'all',
             'title': self.context.translate(_('All')),
             'contentFilter':{},
             'columns': ['title', 
                         'description',
                         'methods']},
        ]

    def getAjaxUrl(self):
        return '/@@get_instruments'

    def getContentFilter(self):
        return {'portal_type': 'Instrument'}

@implementer(ISettingsFactory)
class InstrumentListSettingsFactory(object):
    def __call__(self, context):
        return InstrumentListSettings(context)

@implementer(ISettingsProvider)
class SupplierListSettings(object):
    """
    Table list settings for Suppliers
    """
    def __init__(self, context):
        self.context = context

    def getColumns(self):
        """ Columns definition """
        return {
            'title': {
                'title': _('Supplier'),
                'index': 'sortable_title',
                'toggle': False},
            'description': {
                'title': _('Description'),
                'toggle': True},
        }

    def getStates(self):
        """ Available review states """
        return [
            {'id':'default',
             'title': self.context.translate(_('Active')),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate', 'title': _('Deactivate')}, ],
             'columns': ['title', 
                         'description']},
            {'id':'inactive',
             'title': self.context.translate(_('Dormant')),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate', 'title': _('Activate')}, ],
             'columns': ['title', 
                         'description']},
            {'id':'all',
             'title': self.context.translate(_('All')),
             'contentFilter':{},
             'columns': ['title', 
                         'description']},
        ]

    def getAjaxUrl(self):
        return '/@@get_suppliers'

    def getContentFilter(self):
        return {'portal_type': 'Supplier'}

@implementer(ISettingsFactory)
class SupplierListSettingsFactory(object):
    def __call__(self, context):
        return SupplierListSettings(context)
