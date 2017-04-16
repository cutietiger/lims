# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import mx.lims


class MxLimsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=mx.lims)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'mx.lims:default')


MX_LIMS_FIXTURE = MxLimsLayer()


MX_LIMS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MX_LIMS_FIXTURE,),
    name='MxLimsLayer:IntegrationTesting'
)


MX_LIMS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MX_LIMS_FIXTURE,),
    name='MxLimsLayer:FunctionalTesting'
)


MX_LIMS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MX_LIMS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='MxLimsLayer:AcceptanceTesting'
)
