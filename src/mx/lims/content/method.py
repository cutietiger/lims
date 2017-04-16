# _*_ coding: utf-8 _*_
from zope import schema
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from mx.lims import _

class IMethod(model.Schema):
    """Dexterity Schema for Method
    """
    Instructions = schema.Text(
        title=_(u'Method Instructions'), 
        description=_(u'Technical description and instructions intended for analysts.'))
    ManualEntryOfResults = schema.Bool(
        title=_(u'Manual entry of results'), 
        description=_(u"The results for the Analysis Services that use this method can "
                      u"be set manually"),
        default=False)
    Accredited = schema.Bool(
        title=_(u'Accredited'), 
        description=_(u"Check if the method has been accredited"),
        default=True)
