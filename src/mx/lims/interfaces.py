# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface

class IMxLimsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IInstrumentType(Interface):
    """Explicit marker interface for Instrument Type"""

class IInstrumentTypes(Interface):
    """Explicit marker interface for Instrument Types"""

class IMethod(Interface):
    """Explicit marker interface for Method"""

class IMethods(Interface):
    """Explicit marker interface for Methods"""

class IInstrument(Interface):
    """Explicit marker interface for Instrument"""

class IInstruments(Interface):
    """Explicit marker interface for Instruments"""

class ISupplier(Interface):
    """Explicit marker interface for Supplier"""

class ISuppliers(Interface):
    """Explicit marker interface for Suppliers"""
