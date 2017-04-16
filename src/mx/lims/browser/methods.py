from mx.lims.browser.folderview import FolderView,ajaxFolderData
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from mx.lims.permissions import AddMethod
from Acquisition import aq_parent, aq_inner
from plone.app.uuid.utils import uuidToObject
from plone import api
from mx.lims import _
from mx.lims.adapters.interfaces import IMethodRelations
import ast
import json
import plone
import pdb

class MethodsView(FolderView):
    def __init__(self, context, request):
        super(MethodsView, self).__init__(
            context,request,settings=u'mx.lims.MethodListSettings')
        self.contentFilter = {'portal_type': 'Method',
                              'sort_on': 'sortable_title'}
        self.icon = self.image_url + '/method_big.png'
        self.title = self.context.translate(_('Methods'))
        self.description = ""

    def __call__(self):
        mtool = api.portal.get_tool(name='portal_membership')
        if mtool.checkPermission(AddMethod, self.context):
            self.context_actions[_('Add')] = {
                'url': self.base_url + '/++add++Method'
            }
        return super(MethodsView, self).__call__()

class ajaxGetMethods(ajaxFolderData):
    def __init__(self, context, request):
        super(ajaxGetMethods, self).__init__(
            context,request,settings=u'mx.lims.MethodListSettings')

    def folderitem(self,obj,item,index):
        ok = self.image_url + '/ok.png'
        img = obj.ManualEntryOfResults and ok or ''
        # instruments
        instr = IMethodRelations(obj)
        instruments = instr.getInstruments()
        item['instruments'] = instruments
        item['manual'] = {'image': img}
        return item

class ajaxActivate(BrowserView):
    def __call__(self):
        param = self.request.get('data', None)
        items = ast.literal_eval(param)
        results = []
        wft = api.portal.get_tool(name='portal_workflow')
        for item in items:
            obj = uuidToObject(item['uuid'])
            results.append(obj.title)
            wft.doActionFor(obj, 'activate')
        return results
