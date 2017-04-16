from plone.app.content.browser import tableview
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ListingTable(tableview.Table):
    render = ViewPageTemplateFile("templates/listing_table.pt")
    render_items = ViewPageTemplateFile("templates/listing_table_items.pt")

    def __init__(self, lims_listing=None, table_only=False):
        self.table = self
        self.table_only = table_only
        self.listing = lims_listing
        self.pagesize = lims_listing.pagesize
        folderitems = lims_listing.folderitems()
        if self.pagesize == 0:
            self.pagesize = len(folderitems)
        lims_listing.items = folderitems
        super(ListingTable, self).__init__(
            lims_listing.request,
            lims_listing.base_url,
            lims_listing.view_url,
            folderitems,
            pagesize=self.pagesize)
        self.context = lims_listing.context
        self.form_id = lims_listing.form_id

    def rendered_items(self, cat=None, **kwargs):
        self.cat = cat
        for key, val in kwargs.items():
            self.__setattr__(key, val)
            self.listing.__setattr__(key, val)
        selected_cats = self.listing.selected_cats(self.batch)
        self.this_cat_selected = cat in selected_cats

        self.this_cat_batch = []
        for item in self.batch:
            if item.get('category', 'None') == cat:
                self.this_cat_batch.append(item)

        return self.render_items()

    def tabindex(self):
        i = 0
        while True:
            i += 1
            yield i
