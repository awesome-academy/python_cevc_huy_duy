# =============================================================================
# HTTP API Error Messages
# =============================================================================

class HTTPErrorMessages:
    NOT_FOUND = "The requested resource was not found."
    UNAUTHORIZED = "You are not authorized to access this resource."
    FORBIDDEN = "You do not have permission to perform this action."
    BAD_REQUEST = "The request was invalid or cannot be served."
    INTERNAL_SERVER_ERROR = "An unexpected error occurred on the server."
    METHOD_NOT_ALLOWED = "The request method is not allowed for this endpoint."
    UNPROCESSABLE_ENTITY = "The request was well-formed but was unable to be followed due to semantic errors."
    QUERY_FAILED = "The query could not be executed successfully."
    PAGE_NOT_FOUND = "The requested page was not found."
    TOO_MANY_REQUESTS = "Too many requests. Please try again later."
    SERVICE_UNAVAILABLE = "The service is temporarily unavailable."
    PARSE_ERROR = "Malformed request data."
    AUTHENTICATION_FAILED = "Authentication credentials were not provided or are invalid."
    NOT_AUTHENTICATED = "Authentication credentials were not provided."
    PERMISSION_DENIED = "You do not have permission to perform this action."
    NOT_ACCEPTABLE = "Could not satisfy the request Accept header."
    UNSUPPORTED_MEDIA_TYPE = "Unsupported media type in request."
    THROTTLED = "Request was throttled. Please try again later."
    THROTTLED_WITH_WAIT = "Request was throttled. Please wait {wait} seconds."
    VALIDATION_ERROR = "Invalid input provided."

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
    COORDINATE_RANGE = "This field must be between {min_val} and {max_val} degrees."
    EMAIL_ALREADY_EXISTS = "This email is already in use."
    EMAIL_NOT_FOUND = "Email not found."
    USERNAME_ALREADY_EXISTS = "This username is already in use."
    PASSWORD_MISMATCH = "Password confirmation does not match."
    INVALID_TOKEN = "Invalid token."
    EXPIRED_TOKEN = "Token has expired."
    TOKEN_NOT_PROVIDED = "Authentication token not provided."


# =============================================================================
# Working Space Validation Messages
# =============================================================================

class WorkingSpaceMessages:
    DUPLICATE_NAME_CITY = "Working space with this name and city already exists."
    COORDINATES_REQUIRED = "Both latitude and longitude are required"
    INVALID_COORDINATE_FORMAT = "Invalid latitude or longitude format"
    INVALID_COORDINATE_VALUES = "Invalid coordinate values"
    CREATION_SUCCESS = "Working space created successfully"
    UPDATE_SUCCESS = "Working space updated successfully"
    DELETE_SUCCESS = "Working space deleted successfully"
    NOT_FOUND = "Working space not found"
    DELETE_WITH_DEPENDENCIES = "Cannot delete working space due to existing dependencies"
