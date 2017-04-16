# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides
from mx.lims import _

class IProcedure(model.Schema):

    directives.fieldset(
        'procedure',
        label=_(u'Procedure'),
        fields=('inlab',),
    )

    inlab = schema.Text(
        title=_(u"In-lab calibration procedure"),
        description=_(u"Instructions for in-labe regular calibration ruotines "
                      u"indented for analysts"),
        required=False,
    )

alsoProvides(IProcedure, IFormFieldProvider)
