# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from plone.schema import Email
from mx.lims.content.fields import IAddress
from zope.interface import alsoProvides
from mx.lims import _

class IOrganization(model.Schema):
    TaxNumber = schema.TextLine(
        title=_(u'VAT Number'), 
        required=False) 

    directives.fieldset(
        'address', 
        label=_(u'Address'), 
        fields=['EmailAddress','PhysicalAddress','PostalAddress','BillingAddress'])
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
    BillingAddress = schema.Object(
        title=_(u'Billing Address'), 
        required=False, 
        schema=IAddress)

    directives.fieldset(
        'bank',
        label=_(u'Bank Details'),
        fields=('AccountType','AccountName','AccountNumber','BankName','BankBranch'),
    )

    AccountType = schema.TextLine(
        title=_(u"Account Type"),
        required=False,
    )

    AccountName = schema.TextLine(
        title=_(u"Account Name"),
        required=False,
    )

    AccountNumber = schema.TextLine(
        title=_(u"Account Number"),
        required=False,
    )

    BankName = schema.TextLine(
        title=_(u"Bank Name"),
        required=False,
    )

    BankBranch = schema.TextLine(
        title=_(u"Bank Branch"),
        required=False,
    )

alsoProvides(IOrganization, IFormFieldProvider)
