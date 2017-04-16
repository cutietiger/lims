from mx.lims.browser.folderview import FolderView,ajaxFolderData
from mx.lims.permissions import AddSupplier
from mx.lims.adapters.interfaces import IInstrumentRelations
from plone import api
from mx.lims import _

class SuppliersView(FolderView):
    def __init__(self, context, request):
        super(SuppliersView, self).__init__(
            context,request,settings=u'mx.lims.SupplierListSettings')
        self.contentFilter = {'portal_type': 'Supplier'}
        self.icon = self.image_url + '/supplier_big.png'
        self.title = self.context.translate(_('Suppliers'))
        self.description = ""

    def __call__(self):
        mtool = api.portal.get_tool(name='portal_membership')
        if mtool.checkPermission(AddSupplier, self.context):
            self.context_actions[_('Add')] = {
                'url': self.base_url + '/++add++Supplier'
            }
        return super(SuppliersView, self).__call__()

class ajaxGetSuppliers(ajaxFolderData):
    def __init__(self, context, request):
        super(ajaxGetSuppliers, self).__init__(
            context,request,settings=u'mx.lims.SupplierListSettings')

    def folderitem(self,obj,item,index):
        return item

