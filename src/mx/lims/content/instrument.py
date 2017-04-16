# _*_ coding: utf-8 _*_
from zope import schema
from plone.supermodel import model
from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice
from mx.lims import _

class IInstrument(model.Schema):
    """Dexterity Schema for Instrumet
    """
    InstrumentType = schema.Choice(
        title=_(u'Instrument Type'),
        source=CatalogSource(portal_type='Instrument Type'), 
        )

    Method = RelationChoice(
        title=_(u'Method'),
        source=CatalogSource(portal_type='Method'),
        required=False, 
        )

    Supplier = schema.Choice(
        title=_(u'Supplier'),
        vocabulary=u'mx.lims.vocabularies.Suppliers', 
        required=False, 
        )

