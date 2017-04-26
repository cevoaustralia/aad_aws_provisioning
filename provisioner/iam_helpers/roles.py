"""
Utility functions for AWS IAM role-based activities
"""
import json
import boto3

__iam_client__ = boto3.client('iam')

def add_trust_role(federated_role_template_file, saml_provider_arn, role_name, role_description):
    "Adds a role with the federated identity provider set to `saml_provider_arn`"
    role_definition_base = open(federated_role_template_file, 'rU').read()
    role_definition_json = json.loads(role_definition_base)
    role_definition_json["Statement"][0]["Principal"]["Federated"] = saml_provider_arn
    role_definition = json.dumps(role_definition_json)
    response = __iam_client__.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=role_definition,
        Description=role_description
    )
    return response["Role"]["Arn"]

