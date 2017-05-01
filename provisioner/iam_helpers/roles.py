"""
Utility functions for AWS IAM role-based activities
"""
import json
import boto3
from botocore.exceptions import ClientError
from provisioner.exceptions import TrustRoleExistsError

__iam_client__ = boto3.client('iam')

def add_trust_role(federated_role_template_file, saml_provider_arn, role_name, role_description):
    "Adds a role with the federated identity provider set to `saml_provider_arn`"
    try:
        role_definition_json = json.load(open(federated_role_template_file))
        role_definition_json["Statement"][0]["Principal"]["Federated"] = saml_provider_arn
        role_definition = json.dumps(role_definition_json)
        response = __iam_client__.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=role_definition,
            Description=role_description
        )
        return response["Role"]["Arn"]
    except FileNotFoundError:
        print("Unable to locate template file {}".format(federated_role_template_file))
        raise
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'EntityAlreadyExists':
            print("SAML provider already exists...")
            raise TrustRoleExistsError(role_name)
        else:
            print("Something went wrong creating the Trust Role: {}". format(client_error))
            raise
