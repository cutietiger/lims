from mx.lims.browser.folderview import FolderView,ajaxFolderData
from mx.lims.permissions import AddInstrument
from mx.lims.adapters.interfaces import IInstrumentRelations
from plone import api
from mx.lims import _
import pdb

class InstrumentsView(FolderView):
    def __init__(self, context, request):
        super(InstrumentsView, self).__init__(
            context,request,settings=u'mx.lims.InstrumentListSettings')
        self.contentFilter = {'portal_type': 'Instrument'}
        self.icon = self.image_url + '/instrument_big.png'
        self.title = self.context.translate(_('Instruments'))
        self.description = ""

    def __call__(self):
        mtool = api.portal.get_tool(name='portal_membership')
        if mtool.checkPermission(AddInstrument, self.context):
            self.context_actions[_('Add')] = {
                'url': self.base_url + '/++add++Instrument'
            }
        return super(InstrumentsView, self).__call__()

class ajaxGetInstruments(ajaxFolderData):
    def __init__(self, context, request):
        super(ajaxGetInstruments, self).__init__(
            context,request,settings=u'mx.lims.InstrumentListSettings')

    def folderitem(self,obj,item,index):
        # methods
        m = IInstrumentRelations(obj)
        methods = m.getMethods()
        item['methods'] = methods
        return item

