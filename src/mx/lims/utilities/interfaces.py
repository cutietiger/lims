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

class ISettingsFactory(Interface):
    """Can create settings. """
    def __call__(context):
        """The context provides a location that the settings can make use of
        """
