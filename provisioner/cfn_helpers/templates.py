"""
Collection of functions for working with templates directly
"""

import logging
import boto3
from botocore.exceptions import ClientError
from provisioner.exceptions import InvalidTemplateError

__logger__ = logging.getLogger(__name__)
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
        __logger__.error("Unable to locate template file '%s'", template_path)
        raise
    except ClientError as client_error:
        if client_error.response['Error']['Code'] == 'ValidationError':
            __logger__.warning("SAML provider already exists...")
            raise InvalidTemplateError(template_path, client_error.response['Error']['Message'])
        else:
            __logger__.error("There was an error validating the template: '%s'", str(client_error))
            raise
