# _*_ coding: utf-8 _*_
from zope import schema
from zope import interface
from zope import component
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.schema import Email
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

class IPerson(model.Schema):
    JobTitle = schema.TextLine(
        title=_(u'Job Title')) 
    Department = schema.TextLine(
        title=_(u'Department')) 

    fieldset('address', label=_(u'Address'), 
        fields=['PhysicalAddress','PostalAddress'])
    PhysicalAddress = schema.Object(
        title=_(u'Physical Address'), 
        schema=IAddress)
    PostalAddress = schema.Object(
        title=_(u'Postal Address'), 
        schema=IAddress)

class IOrganization(model.Schema):
    TaxNumber = schema.TextLine(
        title=_(u'VAT Number'), 
        required=False) 

    fieldset('address', label=_(u'Address'), 
        fields=['EmailAddress','PhysicalAddress','PostalAddress'])
    EmailAddress = Email(
        title=_(u'Email Address'), 
        required=False) 
    PhysicalAddress = schema.Object(
        title=_(u'Physical Address'), 
        required=False, 
        schema=IAddress)
    PostalAddress = schema.Object(
        title=_(u'Postal Address'), 
        required=False, 
        schema=IAddress)

class ILab(IOrganization):
    """ Laboratory
    """
