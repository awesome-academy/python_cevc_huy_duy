from functools import wraps
from rest_framework import serializers
from constants.messages import ValidationMessages


def validate_required_string(field_validator):
    @wraps(field_validator)
    def wrapper(self, value):
        if value is None or not value.strip():
            raise serializers.ValidationError(
                ValidationMessages.REQUIRED
            )
        
        stripped_value = value.strip()
        
        return field_validator(self, stripped_value)
    
    return wrapper


def validate_coordinate_range(min_val, max_val):
    def decorator(field_validator):
        @wraps(field_validator)
        def wrapper(self, value):
            if value is not None and (not (min_val <= value <= max_val)):
                raise serializers.ValidationError(
                    ValidationMessages.COORDINATE_RANGE.format(
                        min_val=min_val, 
                        max_val=max_val
                        )
                    )
            
            return field_validator(self, value)
        return wrapper
    return decorator
