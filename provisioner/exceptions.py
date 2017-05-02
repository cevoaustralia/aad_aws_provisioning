"""
Custom errors and errors for IAM helper functions
"""
class Error(Exception):
    """
    Base class for module Error handling
    """
    pass

class SAMLProviderExistsError(Error):
    """
    Error raised when the SAML Provider already exists in the AWS Account
    """
    def __init__(self, provider):
        message = "SAML Provider '{}' already exists in this account.".format(provider)
        super().__init__(message)
        self.provider = provider
        self.message = message

class TrustRoleExistsError(Error):
    """
    Error raised when the trust role already exists in the AWS Account
    """
    def __init__(self, trust_role):
        message = "Trust role '{}' already exists in this account.".format(trust_role)
        super().__init__(message)
        self.trust_role = trust_role
        self.message = message

class RoleNotFoundError(Error):
    """
    Error raised when we can't find a role we look up
    """
    def __init__(self, role_name):
        message = "Could not find role {}".format(role_name)
        super().__init__(message)
        self.role_name = role_name

class StackExistsError(Error):
    """
    Error raised when a Cloudformation stack already exists in the AWS Account
    """
    def __init__(self, provider):
        message = "Stack '{}' already exists in this account.".format(provider)
        super().__init__(message)
        self.provider = provider
        self.message = message

class InvalidTemplateError(Error):
    """
    Error raised when a Cloudformation template is invalid
    """
    def __init__(self, template_path, validation_message):
        message = "Error validating template '{}':\n\n\t {}".format(
            template_path,
            validation_message
            )
        super().__init__(message)
        self.template_path = template_path
        self.validation_message = validation_message


class NoUpdateToPerformError(Error):
    """
    Error raised when there is no update to perform during a stack update
    """
    def __init__(self, stack_name):
        message = "Stack '{}' does not require updating.".format(stack_name)
        super().__init__(message)
        self.stack_name = stack_name
