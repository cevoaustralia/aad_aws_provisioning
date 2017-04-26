"""
Utility functions for dealing with Active Directory approles (from the AWS Application manifest)
"""
import uuid

def generate_ad_role(role_name, role_description, role_arn, saml_provider_arn):
    """
    Generates an AD manifest role dictionary which can be added to the 'appRoles'
    section of the application manifest for the AWS app integration.
    """
    azure_role = "{},{}".format(role_arn, saml_provider_arn)
    role_uuid = str(uuid.uuid4())
    role_blob = {
        "allowedMemberTypes": [
            "User"
        ],
        "displayName": role_name,
        "id":role_uuid,
        "isEnabled": True,
        "description": role_description,
        "value": azure_role
    }
    return role_blob
