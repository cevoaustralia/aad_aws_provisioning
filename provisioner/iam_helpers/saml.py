"""
Utility functions for dealing with AWS IAM SAML stuff
"""
import boto3
from botocore.exceptions import ClientError
from .exceptions import SAMLProviderExistsError

__iam_client__ = boto3.client('iam')

def add_saml_provider(metadata_file_name, saml_provider_name):
    "Creates a new SAML IdP provider in the current account"
    metadata = open(metadata_file_name, 'rU').read()
    try:
        response = __iam_client__.create_saml_provider(
            SAMLMetadataDocument=metadata,
            Name=saml_provider_name
        )
        return response["SAMLProviderArn"]
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'EntityAlreadyExists':
            print("SAML provider already exists...")
            raise SAMLProviderExistsError(saml_provider_name)
        else:
            print("There was an error creating the SAML provider: " + str(client_error))
            raise

def lookup_saml_provider(saml_provider_name):
    "look up the ARN of a SAML provider based on it's name"
    try:
        saml_providers = __iam_client__.list_saml_providers()
    except ClientError as client_error:
        print("Unable to retrieve list of SAML providers: " + str(client_error))
        raise
    else:
        provider_arn = None
        for prov in saml_providers['SAMLProviderList']:
            if saml_provider_name in prov['Arn']:
                provider_arn = prov['Arn']
                break
        else:
            raise ValueError("Couldn't find ARN of SAML Provider " + saml_provider_name)
        return provider_arn
