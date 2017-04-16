from Products.CMFCore.WorkflowCore import WorkflowException
from plone import api
from mx.lims import logger

def doActionFor(instance, action_id):
    actionperformed = False
    message = ''
    workflow = api.portal.get_tool("portal_workflow")
    try:
        workflow.doActionFor(instance, action_id)
        actionperformed = True
    except WorkflowException as e:
        message = str(e)
        logger.warn("Failed to perform transition {} on {}: {}".format(
            action_id, instance, message))
    return actionperformed, message
