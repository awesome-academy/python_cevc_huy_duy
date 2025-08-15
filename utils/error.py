from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.views import exception_handler
from constants.messages import HTTPErrorMessages


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_message = "An error occurred"
        errors = []

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_message = HTTPErrorMessages.BAD_REQUEST
            original_errors = response.data
            if isinstance(original_errors, dict):
                for field, messages in original_errors.items():
                    if isinstance(messages, list):
                        for message in messages:
                            errors.append({"field": field, "message": _(message)})
                    else:
                        errors.append({"field": field, "message": _(messages)})
            elif isinstance(original_errors, list):
                for message in original_errors:
                    errors.append({"field": "non_field_errors", "message": _(message)})
            else:
                errors.append({"field": "non_field_errors", "message": _(original_errors)})
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_message = HTTPErrorMessages.UNAUTHORIZED
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_message = HTTPErrorMessages.FORBIDDEN
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_message = HTTPErrorMessages.NOT_FOUND
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            custom_message = HTTPErrorMessages.INTERNAL_SERVER_ERROR

        response.data = {
            "message": _(custom_message),
            "errors": errors
        }

    return response
