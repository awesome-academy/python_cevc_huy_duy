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
    LOCATION_FILTER_INCOMPLETE = "For location filtering, latitude, longitude, and radius are all required."


# =============================================================================
# Space Validation Messages
# =============================================================================

class SpaceMessages:
    DUPLICATE_NAME_WORKING_SPACE = "Space with this name already exists in this working space."
    INVALID_TIME_RANGE = "Close time must be after open time."
    WORKING_SPACE_NOT_FOUND = "Working space not found."
    CREATION_SUCCESS = "Space created successfully."
    UPDATE_SUCCESS = "Space updated successfully."
    DELETE_SUCCESS = "Space deleted successfully."
    NOT_FOUND = "Space not found."
    DELETE_WITH_DEPENDENCIES = "Cannot delete space due to existing dependencies."
    PRICE_ALL_TYPES_REQUIRED = "You must provide prices for all 3 types: hour, day, month."
    PRICE_HOUR_DAY_MONTH_REQUIRED = "You must provide prices for hour, day, and month."
    DUPLICATE_PRICE_TYPES = "Duplicate price types are not allowed."


# =============================================================================
# Booking Validation Messages
# =============================================================================

class BookingMessages:
    CREATION_SUCCESS = "Booking created successfully."
    UPDATE_SUCCESS = "Booking updated successfully."
    DELETE_SUCCESS = "Booking deleted successfully."
    CANCEL_SUCCESS = "Booking cancelled successfully."
    NOT_FOUND = "Booking not found."
    SPACE_NOT_FOUND = "Space not found."
    UNAUTHORIZED_ACCESS = "You are not authorized to access this booking."
    INVALID_TIME_RANGE = "End time must be after start time."
    INVALID_DATE_RANGE = "Start date must be before end date."
    PAST_START_TIME = "Start time must be in the future."
    TIME_SLOT_OVERLAP = "This time slot overlaps with an existing booking."
    CANNOT_MODIFY_COMPLETED = "Cannot modify a completed booking."
    CANNOT_CANCEL_PAST = "Cannot cancel a booking that has already started."
    ALREADY_CANCELLED = "Booking is already cancelled."
    INVALID_STATUS_TRANSITION = "Invalid status transition."
