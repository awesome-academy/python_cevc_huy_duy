# =============================================================================
# HTTP API Error Messages
# =============================================================================

class HTTPErrorMessages:
    NOT_FOUND = "The requested resource was not found."
    UNAUTHORIZED = "You are not authorized to access this resource."
    FORBIDDEN = "You do not have permission to perform this action."
    BAD_REQUEST = "The request was invalid or cannot be served."
    INTERNAL_SERVER_ERROR = "An unexpected error occurred on the server."

# =============================================================================
# Auth Error Messages
# =============================================================================

class AuthMessages:
    # Registration
    REGISTRATION_SUCCESS = "Registration successful. Please check your email to verify your account."
    REGISTRATION_FAILED = "Registration failed. Please try again."
    
    # Email confirmation
    EMAIL_CONFIRMED_SUCCESS = "Email has been verified successfully."
    EMAIL_CONFIRMATION_SENT = "Verification email has been sent."
    EMAIL_CONFIRMATION_RESENT = "Verification email has been resent."
    ACCOUNT_ALREADY_CONFIRMED = "Account has already been verified."
    
    # Login/Logout
    LOGOUT_SUCCESS = "Logout successful."
    INVALID_CREDENTIALS = "Invalid email or password."
    ACCOUNT_NOT_CONFIRMED = "Account is not verified. Please check your email."


# =============================================================================
# Validation Error Messages
# =============================================================================

class ValidationMessages:
    REQUIRED = "This field is required."
    MIN_LENGTH = "This field must be at least {length} characters long."
    EMAIL_ALREADY_EXISTS = "This email is already in use."
    EMAIL_NOT_FOUND = "Email not found."
    USERNAME_ALREADY_EXISTS = "This username is already in use."
    PASSWORD_MISMATCH = "Password confirmation does not match."
    INVALID_TOKEN = "Invalid token."
    EXPIRED_TOKEN = "Token has expired."
    TOKEN_NOT_PROVIDED = "Authentication token not provided."
