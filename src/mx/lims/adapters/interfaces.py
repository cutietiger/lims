from zope.interface import Interface

class ISettingsProvider(Interface):
    def getColumns():
        """ Get columns
        """
    def getStates():
        """ Get review states
        """
    def getAjaxUrl():
        """ Ajax post url """
    def getContentFilter():
        """ Content Filter """
class IMethodRelations(Interface):
    def getInstruments():
        """ Get all instruments supporting this method
        """
class IInstrumentRelations(Interface):
    def getMethods():
        """ Get all methods this instrument supports
        """
