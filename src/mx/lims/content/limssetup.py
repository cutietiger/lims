# _*_ coding: utf-8 _*_
from zope import schema
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from mx.lims import _

class ILimsSetup(model.Schema):
    """Dexterity Schema for Lims Setup
    """
    fieldset('security', label=_(u'Security'), 
        fields=['PasswordLifetime','AutoLogOff','AllowClerksToEditClients'])
    PasswordLifetime = schema.Int(
        title=_(u'Password lifetime'), 
        description=_(u'The number of days before a password expires. '
                      u'0 disables password expiry'),
        required=True, default=0)
    AutoLogOff = schema.Int(
        title=_(u'Automatic log-off'), 
        description=_(
            u'The number of minutes before a user is automatically logged off.'
            u'0 disables automatic log-off'),
        required=True, default=0)
    AllowClerksToEditClients = schema.Bool(
        title=_(u'Allow Lab Clerks to create and edit clients'), 
        default=False)

    fieldset('accounting', label=_(u'Accounting'), 
        fields=['ShowPrices','Currency'])
    ShowPrices = schema.Bool(
        title=_(u'Include and display pricing information'), 
        default=True)
    Currency = schema.Choice(
        title=_(u'Currency'),
        description=_(u"Select the currency the site will use to display prices."),
        vocabulary=u'mx.lims.vocabularies.Currencies',
        required=True 
        )

    fieldset('analyses', label=_(u'Analyses'), 
        fields=['SamplingWorkflowEnabled','ScheduleSamplingEnabled','ShowPartitions'])
    SamplingWorkflowEnabled = schema.Bool(
        title=_(u'Enable the Sampling workflow'), 
        description=_(u'Select this to activate the sample collection workflow steps.'),
        default=False)
    ScheduleSamplingEnabled = schema.Bool(
        title=_(u'Enable the Schedule a Sampling functionality'), 
        description=_(
            u"Select this to allow a Sampling Coordinator to"
            u" schedule a sampling. This functionality only takes effect"
            u" when 'Sampling workflow' is active"),
        default=False)
    ShowPartitions = schema.Bool(
        title=_(u'Display individual sample partitions'), 
        description=_(u'Turn this on if you want to work with sample partitions'),
        default=True)
