from rest_framework.exceptions import (
    ParseError, AuthenticationFailed, NotAuthenticated,
    PermissionDenied, NotFound, MethodNotAllowed, NotAcceptable,
    UnsupportedMediaType, Throttled, ValidationError
)
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from constants.messages import HTTPErrorMessages
from django.db import DatabaseError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import traceback

import logging

logger = logging.getLogger(__name__)


def _create_error_response(error_type, detail, attr=None):
    return {
        'type': error_type,
        'errors': [{
            'detail': detail,
            'attr': attr
        }]
    }


def _handle_parse_error(exc):
    logger.warning(f"Parse error: {str(exc)}")
    return _create_error_response(
        'parse_error',
        _(HTTPErrorMessages.PARSE_ERROR)
    )


def _handle_authentication_failed(exc):
    logger.warning(f"Authentication failed: {str(exc)}")
    return _create_error_response(
        'authentication_failed',
        _(HTTPErrorMessages.AUTHENTICATION_FAILED)
    )


def _handle_not_authenticated(exc):
    logger.warning(f"Not authenticated: {str(exc)}")
    return _create_error_response(
        'not_authenticated',
        _(HTTPErrorMessages.NOT_AUTHENTICATED)
    )


def _handle_permission_denied(exc):
    logger.warning(f"Permission denied: {str(exc)}")
    return _create_error_response(
        'permission_denied',
        _(HTTPErrorMessages.PERMISSION_DENIED)
    )


def _handle_not_found(exc):
    logger.info(f"Resource not found: {str(exc)}")
    return _create_error_response(
        'not_found',
        _(HTTPErrorMessages.NOT_FOUND)
    )


def _handle_method_not_allowed(exc):
    logger.warning(f"Method not allowed: {str(exc)}")
    return _create_error_response(
        'method_not_allowed',
        _(HTTPErrorMessages.METHOD_NOT_ALLOWED)
    )


def _handle_not_acceptable(exc):
    logger.warning(f"Not acceptable: {str(exc)}")
    return _create_error_response(
        'not_acceptable',
        _(HTTPErrorMessages.NOT_ACCEPTABLE)
    )


def _handle_unsupported_media_type(exc):
    logger.warning(f"Unsupported media type: {str(exc)}")
    return _create_error_response(
        'unsupported_media_type',
        _(HTTPErrorMessages.UNSUPPORTED_MEDIA_TYPE)
    )


def _handle_throttled(exc):
    logger.warning(f"Request throttled: {str(exc)}")
    
    if hasattr(exc, 'wait') and exc.wait:
        detail_message = _(HTTPErrorMessages.THROTTLED_WITH_WAIT).format(wait=exc.wait)
    else:
        detail_message = _(HTTPErrorMessages.THROTTLED)

    return _create_error_response(
        'throttled',
        detail_message
    )


def _handle_validation_error(exc, response):
    logger.warning(f"Validation error: {str(exc)}")
    errors = []

    if hasattr(response, 'data'):
        if isinstance(response.data, dict):
            for field, field_errors in response.data.items():
                if isinstance(field_errors, list):
                    for error in field_errors:
                        errors.append({
                            'detail': str(error),
                            'attr': field
                        })
                else:
                    errors.append({
                        'detail': str(field_errors),
                        'attr': field
                    })
        elif isinstance(response.data, list):
            for error in response.data:
                errors.append({
                    'detail': str(error),
                    'attr': None
                })

    if not errors:
        errors.append({
            'detail': _(HTTPErrorMessages.VALIDATION_ERROR),
            'attr': None
        })

    return {
        'type': 'validation_error',
        'errors': errors
    }


def _handle_generic_api_error(exc):
    logger.error(f"API exception: {str(exc)}")
    return _create_error_response(
        'api_error',
        str(exc) or _(HTTPErrorMessages.BAD_REQUEST)
    )


def _handle_database_error(exc):
    logger.error(f"Database error: {str(exc)}")
    return Response(
        _create_error_response(
            'database_error',
            _(HTTPErrorMessages.INTERNAL_SERVER_ERROR)
        ),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def _handle_object_does_not_exist(exc):
    logger.info(f"Object does not exist: {str(exc)}")
    return Response(
        _create_error_response(
            'not_found',
            _(HTTPErrorMessages.NOT_FOUND)
        ),
        status=status.HTTP_404_NOT_FOUND
    )


def _handle_unhandled_exception(exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())

    return Response(
        _create_error_response(
            'internal_server_error',
            _(HTTPErrorMessages.INTERNAL_SERVER_ERROR)
        ),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        custom_response_data = _handle_drf_exceptions(exc, response)
        response.data = custom_response_data
    else:
        response = _handle_non_drf_exceptions(exc)

    return response


def _handle_drf_exceptions(exc, response):
    exception_handlers = {
        ParseError: _handle_parse_error,
        AuthenticationFailed: _handle_authentication_failed,
        NotAuthenticated: _handle_not_authenticated,
        PermissionDenied: _handle_permission_denied,
        NotFound: _handle_not_found,
        MethodNotAllowed: _handle_method_not_allowed,
        NotAcceptable: _handle_not_acceptable,
        UnsupportedMediaType: _handle_unsupported_media_type,
        Throttled: _handle_throttled,
    }

    for exception_type, handler in exception_handlers.items():
        if isinstance(exc, exception_type):
            return handler(exc)

    if isinstance(exc, ValidationError):
        return _handle_validation_error(exc, response)

    return _handle_generic_api_error(exc)


def _handle_non_drf_exceptions(exc):
    if isinstance(exc, DatabaseError):
        return _handle_database_error(exc)
    elif isinstance(exc, ObjectDoesNotExist):
        return _handle_object_does_not_exist(exc)
    else:
        return _handle_unhandled_exception(exc)


def page_not_found_handler(request, exception=None):
    logger.info(f"404 error: Page not found for URL: {request.path}")

    response_data = {
        "type": "not_found",
        "errors": [{
            "detail": _(HTTPErrorMessages.PAGE_NOT_FOUND),
            "attr": "path"
        }]
    }

    return JsonResponse(response_data, status=404)


def internal_server_error_handler(request):
    logger.error("500 Internal Server Error in Django handler")

    response_data = {
        "type": "internal_server_error",
        "errors": [{
            "detail": _(HTTPErrorMessages.INTERNAL_SERVER_ERROR),
            "attr": None
        }]
    }

    return JsonResponse(response_data, status=500)


def permission_denied_handler(request, exception=None):
    logger.warning(f"403 Permission Denied: {str(exception) if exception else 'Unknown'}")

    response_data = {
        "type": "permission_denied",
        "errors": [{
            "detail": _(HTTPErrorMessages.FORBIDDEN),
            "attr": None
        }]
    }

    return JsonResponse(response_data, status=403)


def bad_request_handler(request, exception=None):
    logger.warning(f"400 Bad Request: {str(exception) if exception else 'Unknown'}")

    response_data = {
        "type": "bad_request",
        "errors": [{
            "detail": _(HTTPErrorMessages.BAD_REQUEST),
            "attr": None
        }]
    }

    return JsonResponse(response_data, status=400)
