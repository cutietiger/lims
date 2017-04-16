from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFPlone.CatalogTool import CatalogTool
from zope.interface import Interface, implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.ZCatalog.ZCatalog import ZCatalog

class ILimsCatalog(Interface):
    """
    """

class LimsCatalog(CatalogTool):
    implements(ILimsCatalog)

    security = ClassSecurityInfo()
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'},)

    title = 'Lims Catalog'
    id = 'lims_catalog'
    portal_type = meta_type = 'LimsCatalog'
    plone_tool = 1

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        portal_types = getToolByName(self, 'portal_types')
        base_types = portal_types.listContentTypes()
        types = [k for k in base_types]
        self.manage_catalogClear()
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.ZopeFindAndApply(portal,
                                obj_metatypes=types,
                                search_sub=True,
                                apply_func=indexObject)

InitializeClass(LimsCatalog)
