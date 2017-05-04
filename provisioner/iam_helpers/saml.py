"""
Utility functions for dealing with AWS IAM SAML stuff
"""
import logging
import boto3
from botocore.exceptions import ClientError
from provisioner.exceptions import SAMLProviderExistsError

__logger__ = logging.getLogger(__name__)
__client__ = boto3.client('iam')

def add_saml_provider(metadata_file_name, saml_provider_name):
    "Creates a new SAML IdP provider in the current account"
    metadata = open(metadata_file_name, 'rU').read()
    try:
        response = __client__.create_saml_provider(
            SAMLMetadataDocument=metadata,
            Name=saml_provider_name
        )
        return response["SAMLProviderArn"]
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'EntityAlreadyExists':
            __logger__.warning("SAML provider already exists...")
            raise SAMLProviderExistsError(saml_provider_name)
        else:
            __logger__.error("There was an error creating the SAML provider: " + str(client_error))
            raise

def look_up_saml_provider(saml_provider_name):
    "look up the ARN of a SAML provider based on it's name"
    try:
        saml_providers = __client__.list_saml_providers()
    except ClientError as client_error:
        __logger__.error("Unable to retrieve list of SAML providers: " + str(client_error))
        raise
    else:
        for prov in saml_providers['SAMLProviderList']:
            if saml_provider_name in prov['Arn']:
                return prov['Arn']

def delete_saml_provider(saml_provider_arn):
    "delete a saml provider"
    try:
        __logger__.debug("Deleting SAML provider '%s'", saml_provider_arn)
        response = __client__.delete_saml_provider(SAMLProviderArn=saml_provider_arn)
        return response
    except ClientError as client_error:
        __logger__.error("Error deleting SAML provider '%s': %s", saml_provider_arn, client_error)
        raise
