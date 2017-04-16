# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides
from mx.lims import _

class ISupplier(model.Schema):
    Website = schema.TextLine(
        title=_(u'Website'), 
        required=False) 

    directives.fieldset(
        'bank',
        label=_(u'Bank Details'),
        fields=('NIB','IBN','SWIFTcode'),
    )

    NIB = schema.TextLine(
        title=_(u"NIB"),
        required=False,
    )

    IBN = schema.TextLine(
        title=_(u"IBN"),
        required=False,
    )

    SWIFTcode = schema.TextLine(
        title=_(u"SWIFT Code"),
        required=False,
    )

alsoProvides(ISupplier, IFormFieldProvider)
