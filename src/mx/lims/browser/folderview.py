from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from mx.lims import _
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.component._api import getMultiAdapter
from Acquisition import aq_parent, aq_inner
from plone.app.uuid.utils import uuidToObject
from .table import ListingTable
from mx.lims import logger
from mx.lims.utils import t, to_utf8, getFromString
from mx.lims.workflow import doActionFor
from mx.lims.utilities.interfaces import ISettingsFactory
import plone
import pdb
import json

class WorkflowAction:
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.destination_url = ''
        self.portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.portal_url = self.portal.absolute_url()

    def _get_form_workflow_action(self):
        """Retrieve the workflow action from the submitted form
            - "workflow_action" is the edit border transition
            - "workflow_action_button" is the bika_listing table buttons
        """
        request = self.request
        form = request.form
        came_from = "workflow_action"
        action = form.get(came_from, '')

        if not action:
            came_from = "workflow_action_button"
            action = form.get('workflow_action_id', '')
            if not action:
                if self.destination_url == "":
                    url = self.context.absolute_url()
                    self.destination_url = request.get_header("referer", url)
                request.response.redirect(self.destination_url)
                return None, None

        # A condition in the form causes Plone to sometimes send two actions
        if type(action) in (list, tuple):
            action = action[0]

        return (action, came_from)

    def _get_selected_items(self, full_objects=True):
        """ return a list of selected form objects
            full_objects defaults to True
        """
        form = self.request.form
        selected_items = {}
        uids = form.get('uids[]', []);
        if type(uids) is str:
            uid = uids
            item = uuidToObject(uid)
            if item:
                selected_items[uid] = item
        else:
            for uid in uids:
                item = uuidToObject(uid)
                if not item:
                    # ignore selected item if object no longer exists
                    continue
                selected_items[uid] = item
        return selected_items

    def workflow_action_default(self, action, came_from):
        if came_from in ['workflow_action', 'edit']:
            # If a single item was acted on we will create the item list
            # manually from this item itself.  Otherwise, bika_listing will
            # pass a list of selected items in the requyest.
            items = [self.context, ]
        else:
            # normal bika_listing.
            items = self._get_selected_items().values()

        if items:
            trans, dest = self.submitTransition(action, came_from, items)
            if trans:
                message = _('Changes saved.')
                self.context.plone_utils.addPortalMessage(message, 'info')
            if dest:
                self.request.response.redirect(dest)
                return
        else:
            message = _('No items selected')
            self.context.plone_utils.addPortalMessage(message, 'warn')

        self.request.response.redirect(self.destination_url)
        return

    def submitTransition(self, action, came_from, items):
        """ Performs the action's transition for the specified items
            Returns (numtransitions, destination), where:
            - numtransitions: the number of objects successfully transitioned.
                If no objects have been successfully transitioned, gets 0 value
            - destination: the destination url to be loaded immediately
        """
        dest = None
        transitioned = []
        workflow = getToolByName(self.context, 'portal_workflow')

        # transition selected items from the bika_listing/Table.
        for item in items:
            # the only actions allowed on inactive/cancelled
            # items are "reinstate" and "activate"
            allowed_transitions = [it['id'] for it in workflow.getTransitionsFor(item)]
            if action in allowed_transitions:
                success = False
                # if action is "verify" and the item is an analysis or
                # reference analysis, check if the if the required number
                # of verifications done for the analysis is, at least,
                # the number of verifications performed previously+1
                success, message = doActionFor(item, action)
                if success:
                    transitioned.append(item.id)
                else:
                    self.context.plone_utils.addPortalMessage(message, 'error')
        return len(transitioned), dest
 
    def __call__(self):
        request = self.request
        form = request.form
        plone.protect.CheckAuthenticator(form)

        if self.destination_url == "":
            self.destination_url = request.get_header("referer",
                                                      self.context.absolute_url())
        action, came_from = self._get_form_workflow_action()
        self.workflow_action_default(action, came_from)

        # Do nothing
        self.request.response.redirect(self.destination_url)

class FolderSettings:
    columns = {
        'obj_type': {'title': _('Type')},
        'id': {'title': _('ID')},
        'title_or_id': {'title': _('Title')},
        'modified': {'title': _('Last modified')},
        'state_title': {'title': _('State')},
    }
    # review_state
    #
    # A list of dictionaries, specifying parameters for listing filter buttons.
    # - If review_state[x]['transitions'] is defined it's a list of dictionaries:
    #     [{'id':'x'}]
    # Transitions will be ordered by and restricted to, these items.
    #
    # - If review_state[x]['custom_actions'] is defined. it's a list of dict:
    #     [{'id':'x'}]
    # These transitions will be forced into the list of workflow actions.
    # They will need to be handled manually in the appropriate WorkflowAction
    # subclass.
    review_states = [
        {
            'id': 'default',
            'contentFilter': {},
            'title': _('All'),
            'columns': ['obj_type', 'title_or_id', 'modified', 'state_title']
        },
    ]
 
class FolderView(BrowserView):
    """Base View for Lims Table Listings
    """
    template = ViewPageTemplateFile("templates/folder.pt")

    # The name of the catalog which be searched for results mtaching self.contentFilter
    catalog = "portal_catalog"

    # This is the list of query parameters passed to the catalog.
    # It's just a default set.  This can be modified by Python, or by the
    # contentFilter key in self.review_states.
    contentFilter = {}

    allow_edit = True

    # Use the context_actions to show a list of buttons above the List
    # The "Add" button is usually inserted here.
    context_actions = {}

    # Display the left-most column for selecting all/individual items
    show_select_column = False

    show_select_all_checkbox = True

    # This is the column used to hold the handles used to manually re-order items in the list
    show_sort_column = False

    # Workflow action buttons (and anything hacked into that list of actions)
    show_workflow_action_buttons = True

    # Column toggles are displayed when right-clicking on the column headers.
    # Set this to false to disallow setting column toggles for some reason.
    show_column_toggles = True

    # setting pagesize to 0 specifically disables the batch size dropdown.
    pagesize = 30

    # select checkbox is normally called uids:list
    # if table_only is set then the context form tag might require
    # these to have a different name=FieldName:list.
    # This is a cheat and we can ignore it.
    select_checkbox_name = "uids"

    # when rendering multiple lims_listing tables, form_id must be unique
    form_id = "list"
    review_state = 'default'

    # Show categorized list; categories are collapsed until required
    show_categories = False

    # These are the possible categories.  If self.show_categories is True,
    # These are the categories which will be rendered.  Any items without
    # a 'category' key/value will be shown in a special "None" category.
    categories = []

    # By default every category will be expanded.  Careful with this, if there
    # is a possibility that the list could get very large.
    expand_all_categories = False

    # With this setting, we allow categories to be simple empty place-holders.
    # When activated, the category data will be fetched from the server,
    # and completed inline.  This is useful for list which will have many
    # thousands of entries in many categories, where loading the entire list
    # in HTML would be very slow.
    # If you want to use service categories set this option ajax_categories_url
    ajax_categories = False

    # using the following attribute, some python class may add a CSS class
    # to the TH elements used for the category headings.  This allows all
    # manner of Javascript trickery.
    cat_header_class = ''

    # category_index is the catalog index from each listed object.
    # it will be used to decide if an item is a member of a category.
    # This is required, if using ajax_categories.
    category_index = None

    # A list of fields, and the icons that should be shown in them.
    field_icons = {}

    show_table_footer = True

    # Sort with JS when a column does not have an index associated.
    # It's not useful if the table is paginated since
    # it only searches visible items
    manual_sort_on = None

    columns = {}

    # Additional indexes to be searched
    # any index name not specified in self.columns[] can be added here.
    filter_indexes = ['Title', 'Description', 'SearchableText']

    # The current or default review_state when one hasn't been selected.
    # With this setting, LimsListing instances must be careful to change it,
    # without having valid review_state existing in self.review_states
    default_review_state = 'default'

    # review_state
    #
    # A list of dictionaries, specifying parameters for listing filter buttons.
    # - If review_state[x]['transitions'] is defined it's a list of dictionaries:
    #     [{'id':'x'}]
    # Transitions will be ordered by and restricted to, these items.
    #
    # - If review_state[x]['custom_actions'] is defined. it's a list of dict:
    #     [{'id':'x'}]
    # These transitions will be forced into the list of workflow actions.
    # They will need to be handled manually in the appropriate WorkflowAction
    # subclass.
    review_states = []

    # The advanced filter bar instance, it is initialized using
    # getAdvancedFilterBar
    _advfilterbar = None

    def __init__(self, context, request, **kwargs):
        super(FolderView, self).__init__(context, request)
        path = hasattr(context, 'getPath') and context.getPath() \
            or "/".join(context.getPhysicalPath())
        if hasattr(self, 'contentFilter'):
            if not 'path' in self.contentFilter:
                self.contentFilter['path'] = {"query": path, "level" : 0 }
        else:
            if not 'path' in self.contentFilter:
                self.contentFilter = {'path': {"query": path, "level" : 0 }}
        portal = api.portal.get()
        self.portal_url = portal.absolute_url()
        self.image_url = self.portal_url + '/++resource++mx.lims.images'
        self.base_url = context.absolute_url()
        self.view_url = self.base_url
        self.show_all = False
        self.show_more = False
        self.limit_from = 0
        # get settings from specified utility (e.g., Methods)
        if 'settings' in kwargs:
            settingsFac = getUtility(ISettingsFactory, kwargs['settings'])
            self.settings = settingsFac(context)
            self.columns = self.settings.getColumns()
            self.review_states = self.settings.getStates()

    @property
    def review_state(self):
        key = '%s_review_state' % self.form_id
        state_id = self.request.form.get(key, self.default_review_state)
        states = [r for r in self.review_states if r['id'] == state_id]
        if not states:
            logger.error('%s.review_states does not contain key: %s' %
                         (self, state_id))
            return None
        review_state = states[0] if states else self.review_states[0]
        self.request.form[key] = review_state['id']
        return review_state

    def _process_request(self):
        form_id = self.form_id
        catalog = getToolByName(self.context, self.catalog)
        self.limit_from = int(self.request.get(form_id + '_limit_from', 0))

        #contentFilter is allowed in every self.review_state
        for k, v in self.review_state.get('contentFilter', {}).items():
            self.contentFilter[k] = v

        self.sort_on = self.sort_on \
            if hasattr(self, 'sort_on') and self.sort_on \
            else None
        self.sort_on = self.request.get(form_id + '_sort_on', self.sort_on)
        self.sort_order = self.request.get(form_id + '_sort_order', 'ascending')
        self.manual_sort_on = self.request.get(form_id + '_manual_sort_on', None)

        if self.sort_on:
            if self.sort_on in self.columns.keys():
                if self.columns[self.sort_on].get('index', None):
                    self.request.set(form_id + '_sort_on', self.sort_on)
                    idx = self.columns[self.sort_on]['index']
                    self.sort_on = idx
                    self.manual_sort_on = None
                else:
                    self.manual_sort_on = self.sort_on
            else:
                self.sort_on = None

        if self.sort_on or self.manual_sort_on:
            # By default, if sort_on is set, sort the items ASC
            # Trick to allow 'descending' keyword instead of 'reverse'
            self.sort_order = 'reverse' if self.sort_order \
                                        and self.sort_order[0] in ['d', 'r'] \
                                        else 'ascending'
        self.contentFilter['sort_order'] = self.sort_order

        if self.sort_on:
            # Ensure we have a valid sort_on index is valid
            if self.sort_on in catalog.indexes():
                self.contentFilter['sort_on'] = self.sort_on

        pagesize = self.request.get(form_id + '_pagesize', self.pagesize)
        if type(pagesize) in (list, tuple):
            pagesize = pagesize[0]
        try:
            pagesize = int(pagesize)
        except:
            pagesize = self.pagesize = 10

        # Plone's batching wants this variable
        self.request.set('pagesize', self.pagesize)
        self.request.set(self.form_id + '_pagesize', self.pagesize)

    def GET_url(self, include_current=True, **kwargs):
        url = self.request['URL'].split("?")[0]
        # take values from form (both html form and GET request slurped here)
        query = {}
        if include_current:
            for k, v in self.request.form.items():
                if k.startswith(self.form_id + "_") and "uids" not in k:
                    query[k] = v

        # override from self attributes
        for x in "pagesize", "review_state", "sort_order", "sort_on", "limit_from":
            if str(getattr(self, x, None)) != 'None':
                # I don't understand why on AR listing, getattr(self,x)
                # is a dict, but this line will resolve LIMS-1420
                if x == "review_state" and type(getattr(self, x)) == dict:
                    query['%s_%s' % (self.form_id, x)] = getattr(self, x)['id']
                else:
                    query['%s_%s' % (self.form_id, x)] = getattr(self, x)

        # then override with passed kwargs
        for x in kwargs.keys():
            query['%s_%s' % (self.form_id, x)] = kwargs.get(x)
        if query:
            url = url + "?" + "&".join(["%s=%s" % (x, y) for x, y in query.items()])
        return url

    def __call__(self):
        self._process_request()
        return self.template()

    # Used to return json for datatable options
    def options(self):
        # ajax post
        url = self.base_url + self.settings.getAjaxUrl()
        ajaxopt = {'url': url, 'type': 'POST'}
        # i18n
        lang = {'url': self.portal_url + '/++resource++mx.lims/locales/Chinese.json'}
        # columns
        columns = []
        selectitem = {'defaultContent': '', 'orderable': False}
        columns.append(selectitem)
        review_state_id = self.request.get('list_review_state', 'default');
        review_state = [t for t in self.review_states if t['id'] == review_state_id];
        review_state = review_state and review_state[0] or self.review_states[0];
        for column in review_state['columns']:
            item = {'data': column }
            if not self.columns[column].get('index', None):
                item['orderable'] = False
            columns.append(item)
        states = [{'id': s['id'], 'title': s['title'], 
                   'url': self.GET_url(review_state=s['id'])} for s in self.review_states]
        opts = {
            # server side processing
            'serverSide': True,
            'ajax': ajaxopt,
            # remote language file
            'language': lang,
            # default order
            'order': [[1, 'asc']],
            # columns
            'columns': columns,
            'state_id': self.review_state,
            'review_states': states
        }
        return json.dumps(opts)

    def get_transitions_for_items(self, items):
        """Extract Worfklow transitions for the bika listing items
        """
        workflow = api.portal.get_tool('portal_workflow')
        out = {}

        # helper method to extract the object from an bika listing item
        def get_object_from_item(item):
            obj = item.get("obj")
            if hasattr(obj, "getObject") and callable(obj.getObject):
                return obj.getObject()
            return obj

        # extract all objects from the items
        objects = map(get_object_from_item, self.items)

        for obj in objects:
            for transition in workflow.getTransitionsFor(obj):
                # append the transition by its id to the transitions dictionary
                out[transition['id']] = transition
        return out

    def get_workflow_actions_current(self):
        # The actions which will be displayed in the listing view
        actions = []

        if 'transitions' in self.review_state:
            for transition in self.review_state['transitions']:
                actions.append(transition)
        else:
            for state in self.review_states:
                if 'transitions' in state:
                    for transition in state['transitions']:
                        actions.append(transition)

        return actions

    def get_workflow_actions(self):
        """ Compile a list of possible workflow transitions for items
            in this Table.
        """
        # cbb return empty list if we are unable to select items
        if not self.show_select_column:
            return []

        if not hasattr(self,'items') or len(self.items) == 0:
            return []

        # get all transitions for all items.
        transitions = self.get_transitions_for_items(self.items)

        # The actions which will be displayed in the listing view
        actions = []

        # the list is restricted to and ordered by these transitions.
        if 'transitions' in self.review_state:
            for transition in self.review_state['transitions']:
                if transition['id'] in transitions:
                    actions.append(transitions[transition['id']])
        else:
            actions = transitions.values()

        new_actions = []
        # remove any invalid items with a warning

        for action in actions:
            if isinstance(action, dict) and 'id' in action:
                new_actions.append(action)

        actions = new_actions

        # and these are removed
        if 'hide_transitions' in self.review_state:
            actions = [a for a in actions
                       if a['id'] not in self.review_state['hide_transitions']]

        # cheat: until workflow_action is abolished, all URLs defined in
        # GS workflow setup will be ignored, and the default will apply.
        # (that means, WorkflowAction-bound URL is called).
        for action in actions:
            action['url'] = ''

        # if there is a self.review_state['some_state']['custom_actions'] attribute
        # on the BikaListingView, add these actions to the list.
        if 'custom_actions' in self.review_state:
            for action in self.review_state['custom_actions']:
                if isinstance(action, dict) and 'id' in action:
                    actions.append(action)

        # # translate the workflow action title for the template
        # for action in actions:
        #     action['title'] = t(_(action['title']))
        return actions

    def folderitem(self, obj,item, index):
        return item

    def folderitems(self, full_objects = False):
        #self.contentsMethod = self.context.getFolderContents
        if not hasattr(self, 'contentsMethod'):
            self.contentsMethod = getToolByName(self.context, self.catalog)
        context = aq_inner(self.context)

        #misc. tools
        plone_layout = getMultiAdapter((context, self.request), name=u'plone_layout')
        plone_utils = getToolByName(context, 'plone_utils')
        portal_types = getToolByName(context, 'portal_types')
        workflow = getToolByName(context, 'portal_workflow')

        show_all = False

        brains = self.contentsMethod(self.contentFilter)
        idx = 0
        results = []
        self.show_more = False
        for i, brain in enumerate(brains):
            # avoid creating unnecessary info for items outside the current
            # batch;  only the path is needed for the "select all" case...
            # we only take allowed items into account
            if not show_all and idx >= self.pagesize:
                # Maximum number of items to be shown reached!
                self.show_more = True
                break

            obj = brain.getObject()
            if not obj or not self.isItemAllowed(obj):
                continue

            # we don't know yet if it's a brain or an object
            path = hasattr(obj, 'getPath') and obj.getPath() or \
                 "/".join(obj.getPhysicalPath())

            uid = obj.UID()
            title = obj.Title()
            description = obj.Description()
            url = obj.absolute_url()
            relative_url = obj.absolute_url(relative=True)
            icon = plone_layout.getIcon(obj)

            fti = portal_types.get(obj.portal_type)

            if fti is not None:
                type_title_msgid = fti.Title()
            else:
                type_title_msgid = obj.portal_type

            url_href_title = '%s at %s: %s' % (
                t(type_title_msgid),
                path,
                to_utf8(description))

            modified = api.portal.get_localized_time(obj.modified())
            type_class = 'contenttype-' + \
                plone_utils.normalizeString(obj.portal_type)
            state_class = ''
            states = {}

            results_dict = dict(
                obj=obj,
                id=obj.getId(),
                title=title,
                uid=uid,
                path=path,
                url=url,
                fti=fti,
                item_data=json.dumps([]),
                url_href_title=url_href_title,
                obj_type=obj.Type,
                size=obj.getObjSize,
                modified=modified,
                icon=icon.html_tag(),
                type_class=type_class,
                choices={},
                state_class=state_class,
                relative_url=relative_url,
                view_url=url,
                table_row_class="",
                category='None',
                allow_edit=[],
                required=[],
                field={},
                before={},
                after={},
                replace={},
            )

            # extra classes for individual fields on this item { field_id : "css classes" }
            results_dict['class'] = {}
            # Search for values for all columns in obj

            for key in self.columns.keys():
                # if the key is already in the results dict
                # then we don't replace it's value
                value = results_dict.get(key, '')
                if key not in results_dict:
                    attrobj = getFromString(obj, key)
                    value = attrobj if attrobj else value

                    # Custom attribute? Inspect to set the value
                    # for the current column dinamically
                    vattr = self.columns[key].get('attr', None)
                    if vattr:
                        attrobj = getFromString(obj, vattr)
                        value = attrobj if attrobj else value
                    results_dict[key] = value

                # Replace with an url?
                replace_url = self.columns[key].get('replace_url', None)
                if replace_url:
                    attrobj = getFromString(obj, replace_url)
                    if attrobj:
                        results_dict['replace'][key] = \
                            '<a href="%s">%s</a>' % (attrobj, value)

            # The item basics filled. Delegate additional actions to folderitem
            # service. folderitem service is frequently overriden by child objects
            item = self.folderitem(obj, results_dict, idx)
            if item:
                results.append(item)
                idx += 1

        return results

    def contents_table(self, table_only=False):
        """ If you set table_only to true, then nothing outside of the
            <table/> tag will be printed (form tags, authenticator, etc).
            Then you can insert your own form tags around it.
        """
        table = ListingTable(lims_listing=self, table_only=table_only)
        return table.render(self)

    def selected_cats(self, items):
        """Return a list of categories that will be expanded by default when
        the page is reloaded.

        In this default method, categories which contain selected
        items are always expanded.

        :param items: A list of items returned from self.folderitems().
        :return: a list of strings, self.categories contains the complete list.
        """
        cats = []
        for item in items:
            cat = item.get('category', 'None')
            if item.get('selected', False) \
                or self.expand_all_categories \
                or not self.show_categories:
                if cat not in cats:
                    cats.append(cat)
        return cats

    def restricted_cats(self, items):
        """Return a list of categories that will not be displayed.

        The items will still be present, and account for a part of the page
        batch total.

        :param items: A list of items returned from self.folderitems().
        :return: a list of AnalysisCategory instances.
        """
        return []

    def isItemAllowed(self, obj):
        """ return if the item can be added to the items list.
        """
        return True 

class ajaxFolderData(object):
    def __init__(self, context, request, **kwargs):
        self.context = context
        self.request = request
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        self.image_url = portal_url + '/++resource++mx.lims.images'
        # get settings from specified utility (e.g., Methods)
        if 'settings' in kwargs:
            settingsFac = getUtility(ISettingsFactory, kwargs['settings'])
            self.settings = settingsFac(context)
            self.columns = self.settings.getColumns()
            self.review_states = self.settings.getStates()

    def folderitem(self,obj,item,index):
        return item

    def isItemAllowed(self, obj):
        """ return if the item can be added to the items list.
        """
        return True

    def __call__(self):
        # process request
        draw = int(self.request.get('draw', ''))
        start = int(self.request.get('start', ''))
        length = int(self.request.get('length', ''))
        orderid = self.request.get('order[0][column]', '')
        direction = self.request.get('order[0][dir]', '')
        column = self.request.get('columns[%s][data]' % orderid, '')
        state_id = self.request.get('inactive_state', '')
        states = [r for r in self.review_states if r['id'] == state_id]
        review_state = states[0] if states else self.review_states[0]
        search = self.request.get('search[value]', '')

        # query results
        catalog = api.portal.get_tool(name='portal_catalog')
        contentFilter = self.settings.getContentFilter()
        if column:
            if column in self.columns.keys():
                if self.columns[column].get('index', None):
                    contentFilter['sort_on'] = self.columns[column]['index']
                    contentFilter['sort_order'] = direction == 'asc' and 'ascending' or 'reverse'
        # inactive_state
        for k, v in review_state.get('contentFilter', {}).items():
            contentFilter[k] = v

        # full text search
        if search:
            contentFilter['SearchableText'] = search

        brains = catalog(contentFilter)
        # get number of items
        num_items = len(brains)
        # start from specified index         
        brains = brains[start:]
        items = []
        idx = 0
        for i, brain in enumerate(brains):
            if idx >= length:
                break
            # get the underlying object
            obj = brain.getObject()
            if not self.isItemAllowed(obj):
                continue
            # get attributes
            uid = obj.UID()
            title = obj.Title()
            description = obj.Description()
            url = obj.absolute_url()
            # available actions for this object
            actions = self.get_workflow_actions(obj)
            item = {
                'title': {'url': url, 'title': title},
                'description': description,
                'uuid': uid,
                'valid_transitions': ','.join(actions),
            }
            # The item basics filled. Delegate additional actions to folderitem
            # service. folderitem service is frequently overriden by child objects
            item = self.folderitem(obj, item, i)
            idx += 1
            items.append(item)

        result = {
            'draw': draw,
            'recordsTotal': num_items,
            'recordsFiltered': num_items,
            'data': items
        }
        return json.dumps(result)

    def get_workflow_actions(self, obj):
        workflow = api.portal.get_tool('portal_workflow')
        return [t['id'] for t in workflow.getTransitionsFor(obj)]
