# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from mx.lims.permissions import *
from mx.lims.config import SITE_STRUCTURE
from plone import api

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'mx.lims:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

def constrain_types(folder, addable_types):
    """Constrain addable types in folder.
    """
    folder.setConstrainTypesMode(True)
    folder.setImmediatelyAddableTypes(addable_types)
    folder.setLocallyAllowedTypes(addable_types)

class LimsGenerator:
    def setupGroupsAndRoles(self, portal):
       # Create groups
        portal_groups = portal.portal_groups

        if 'LabManagers' not in portal_groups.listGroupIds():
            portal_groups.addGroup('LabManagers', title="Lab Managers",
                roles=['Member', 'LabManager', 'Site Administrator', ])

        if 'LabClerks' not in portal_groups.listGroupIds():
            portal_groups.addGroup('LabClerks', title="Lab Clerks",
                roles=['Member', 'LabClerk'])

    def setupPermissions(self, portal):
        """ Set up some suggested role to permission mappings.
        """
        # Root permissions
        mp = portal.manage_permission
        mp(AddAnalysisProfile, ['Manager', 'Owner', 'LabManager', 'LabClerk'], 1)
        mp(AddMethod, ['Manager', 'Owner', 'LabManager'], 1)

    def create_site_structure(self, root, structure):
        """Create and publish new site structure as defined in config.py."""
        for item in structure:
            id = item['id']
            title = item['title']
            description = item.get('description', u'')

            if id not in root:
                if 'creators' not in item:
                    item['creators'] = (u'admin',)
                obj = api.content.create(root, **item)
                # publish private content or make a workflow transition
                if item['type'] not in ['Image', 'File']:
                    if '_transition' not in item and api.content.get_state(obj) == 'private':
                        api.content.transition(obj, 'publish')
                    elif item.get('_transition', None):
                        api.content.transition(obj, item['_transition'])
                # constrain types in folder?
                if '_addable_types' in item:
                    constrain_types(obj, item['_addable_types'])
                # the content has more content inside? create it
                if '_children' in item:
                    self.create_site_structure(obj, item['_children'])
                # set the default view to object
                if '_layout' in item:
                    obj.setLayout(item['_layout'])
                # XXX: workaround for https://github.com/plone/plone.api/issues/99
                obj.setTitle(title)
                obj.setDescription(description)
                obj.reindexObject()

def setupVarious(context):
    """
    Final LIMS import steps.
    """
    portal = api.portal.get()
    site = context.getSite()
    gen = LimsGenerator()
    gen.setupGroupsAndRoles(site)
    gen.setupPermissions(site)
    gen.create_site_structure(portal, SITE_STRUCTURE)
