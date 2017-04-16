# -*- coding: utf-8 -*-
from plone import api

import logging

default_profile = 'profile-mx.lims:default'
logger = logging.getLogger(__name__)

def upgrade_workflow(setup):
    setup.runImportStepFromProfile(default_profile, 'workflow')
    portal = api.portal.get()
    methods_folder = portal['methods']

    methods_url = methods_folder.absolute_url()

    wft = api.portal.get_tool(name='portal_workflow')
    # Find all methods
    brains = api.content.find(portal_type='Method')
    for brain in brains:
        obj = brain.getObject()
        logger.info('Initialize {} workflow state'.format(obj.absolute_url()))
        wft.doActionFor(obj, 'deactivate')

def upgrade_registry(setup):
    setup.runImportStepFromProfile(default_profile, 'plone.app.registry')

def upgrade_type(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')

def upgrade_instruments(setup):
    setup.runImportStepFromProfile(default_profile, 'rolemap')
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    setup.runImportStepFromProfile(default_profile, 'controlpanel')
    setup.runImportStepFromProfile(default_profile, 'workflow')
    portal = api.portal.get()
    setup_folder = portal['lims_setup']
    item = dict(
        type='Instruments',
        id='instruments',
        title=u'Instruments',
        excludeFromNav=True)
    obj = api.content.create(setup_folder, **item)
    obj.setTitle(item['title'])
    obj.reindexObject()
    
def upgrade_suppliers(setup):
    setup.runImportStepFromProfile(default_profile, 'rolemap')
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    setup.runImportStepFromProfile(default_profile, 'controlpanel')
    setup.runImportStepFromProfile(default_profile, 'workflow')
    portal = api.portal.get()
    setup_folder = portal['lims_setup']
    item = dict(
        type='Suppliers',
        id='suppliers',
        title=u'Suppliers',
        excludeFromNav=True)
    obj = api.content.create(setup_folder, **item)
    obj.setTitle(item['title'])
    obj.reindexObject()
