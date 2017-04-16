# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from mx.lims.testing import MX_LIMS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that mx.lims is properly installed."""

    layer = MX_LIMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mx.lims is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'mx.lims'))

    def test_browserlayer(self):
        """Test that IMxLimsLayer is registered."""
        from mx.lims.interfaces import (
            IMxLimsLayer)
        from plone.browserlayer import utils
        self.assertIn(IMxLimsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MX_LIMS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['mx.lims'])

    def test_product_uninstalled(self):
        """Test if mx.lims is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'mx.lims'))

    def test_browserlayer_removed(self):
        """Test that IMxLimsLayer is removed."""
        from mx.lims.interfaces import IMxLimsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMxLimsLayer, utils.registered_layers())
