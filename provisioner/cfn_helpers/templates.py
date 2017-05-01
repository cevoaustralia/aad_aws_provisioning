"""
Collection of functions for working with templates directly
"""

import boto3

__client__ = boto3.client('cloudformation', region_name='ap-southeast-2')

def validate_template(template):
    """
    Validate a template is correct.
    """
    response = __client__.validate_template(TemplateBody=template)

    return response
