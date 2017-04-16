from mx.lims.controlpanel.instruments import InstrumentsView

class SupplierInstrumentsView(InstrumentsView):
    def __init__(self, context, request):
        super(SupplierInstrumentsView).__init(context,request,settings='')

    def isItemAllowed(self, obj):
        supp = obj.Supplier if obj else None
        return supp == self.context.UID() if supp else None
