"""
Custom errors and exceptions for IAM helper functions
"""
class Error(Exception):
    """
    Base class for module Error handling
    """
    pass

class SAMLProviderExistsError(Error):
    """
    Exception raised when the SAML Provider already exists in the AWS Account
    """
    def __init__(self, provider):
        message = "SAML Provider '{}' already exists in this account.".format(provider)
        super().__init__(message)
        self.provider = provider
        self.message = message

class TrustRoleExistsError(Error):
    """
    Exception raised when the trust role already exists in the AWS Account
    """
    def __init__(self, trust_role):
        message = "Trust role '{}' already exists in this account.".format(trust_role)
        super().__init__(message)
        self.trust_role = trust_role
        self.message = message

class StackExistsError(Error):
    """
    Exception raised when a Cloudformation stack already exists in the AWS Account
    """
    def __init__(self, provider):
        message = "Stack '{}' already exists in this account.".format(provider)
        super().__init__(message)
        self.provider = provider
        self.message = message

class InvalidTemplateError(Error):
    """
    Exception raised when a Cloudformation template is invalid
    """
    def __init__(self, template_path, validation_message):
        message = "Error validating template '{}':\n\n\t {}".format(
            template_path,
            validation_message
            )
        super().__init__(message)
        self.template_path = template_path
        self.validation_message = validation_message
