# -*- coding: utf-8 -*-
from mx.lims.interfaces import IInstrumentType, IInstrumentTypes
from mx.lims.interfaces import IMethod, IMethods
from mx.lims.interfaces import IInstrument, IInstruments
from mx.lims.interfaces import ISupplier, ISuppliers
from plone.dexterity.content import Container, Item
from zope.interface import implementer

@implementer(IInstrumentType)
class InstrumentType(Item):
    """Convenience subclass for ``Instrument Type`` portal type
    """

@implementer(IInstrumentTypes)
class InstrumentTypes(Container):
    """Convenience subclass for ``Instrument Types`` portal type
    """
@implementer(IMethod)
class Method(Item):
    """Convenience subclass for ``Method`` portal type
    """

@implementer(IMethods)
class Methods(Container):
    """Convenience subclass for ``Methods`` portal type
    """

@implementer(IInstrument)
class Instrument(Container):
    """Convenience subclass for ``Instrument`` portal type
    """

@implementer(IInstruments)
class Instruments(Container):
    """Convenience subclass for ``Instruments`` portal type
    """
@implementer(ISupplier)
class Supplier(Container):
    """Convenience subclass for ``Supplier`` portal type
    """

@implementer(ISuppliers)
class Suppliers(Container):
    """Convenience subclass for ``Suppliers`` portal type
    """
