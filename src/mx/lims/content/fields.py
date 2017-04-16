# _*_ coding: utf-8 _*_
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from z3c.form.object import registerFactoryAdapter
from mx.lims import _

class IAddress(model.Schema):
    street = schema.TextLine(
        title=_(u'Street Address'),
        description=_(u'Street Address.'),
        required=False,
        default=None
    )
    postal = schema.TextLine(
        title=_(u'Zip Code'),
        description=_(u'Zip or Postal Code.'),
        required=False,
        default=None
    )

@implementer(IAddress)
class Address(object):
    street = FieldProperty(IAddress['street'])
    postal = FieldProperty(IAddress['postal'])

registerFactoryAdapter(IAddress,Address)
