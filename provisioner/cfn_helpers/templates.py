"""
Collection of functions for working with templates directly
"""

import boto3
from botocore.exceptions import ClientError
from provisioner.exceptions import InvalidTemplateError

__client__ = boto3.client('cloudformation', region_name='ap-southeast-2')

def validate_template(template_path):
    """
    Validate a template is correct.
    """
    try:
        with open(template_path, 'r') as template_body:
            response = __client__.validate_template(TemplateBody=template_body.read())
            return response
    except FileNotFoundError:
        print("Unable to locate template file {}".format(template_path))
        raise
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'ValidationError':
            print("SAML provider already exists...")
            raise InvalidTemplateError(template_path, client_error.response['Error']['Message'])
        else:
            print("There was an error validating the template: " + str(client_error))
            raise
