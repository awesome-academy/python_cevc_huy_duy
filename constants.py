from django.db import models

# =============================================================================
# User Related Constants
# =============================================================================

class UserStatusChoices(models.TextChoices):
    REGISTER = 'register', 'Register'
    ACTIVATED = 'activated', 'Activated'
    DEACTIVATED = 'deactivated', 'Deactivated'


# =============================================================================
# Working Space Related Constants
# =============================================================================

class WorkingSpaceManagerRoleChoices(models.TextChoices):
    MANAGER = 'manager', 'Manager'
    ADMIN = 'admin', 'Admin'
    OWNER = 'owner', 'Owner'


# =============================================================================
# Space Related Constants
# =============================================================================

class SpaceStatusChoices(models.TextChoices):
    WAITING = 'waiting', 'Waiting'
    BLOCKED = 'blocked', 'Blocked'
    ACTIVATED = 'activated', 'Activated'


class SpaceTypeChoices(models.TextChoices):
    PRIVATE_OFFICE = 'private_office', 'Private Office'
    WORKING_DESK = 'working_desk', 'Working Desk'


# =============================================================================
# Amenity Related Constants
# =============================================================================

class AmenityStatusChoices(models.TextChoices):
    WAITING = 'waiting', 'Waiting'
    BLOCKED = 'blocked', 'Blocked'
    ACTIVATED = 'activated', 'Activated'


# =============================================================================
# Pricing Related Constants
# =============================================================================

class PriceTypeChoices(models.TextChoices):
    MONTH = 'month', 'Month'
    DAY = 'day', 'Day'
    HOUR = 'hour', 'Hour'


# =============================================================================
# Booking Related Constants
# =============================================================================

class BookingStatusChoices(models.TextChoices):
    PROCESSING = 'processing', 'Processing'
    SUCCEEDED = 'succeeded', 'Succeeded'
    CANCELED = 'canceled', 'Canceled'


# =============================================================================
# Membership Related Constants
# =============================================================================

class MemberStatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DEACTIVE = 'deactive', 'Deactive'


# =============================================================================
# Payment Related Constants
# =============================================================================

class PaymentStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'


class PaymentTypeChoices(models.TextChoices):
    NEW = 'new', 'New'
    RENEWALS = 'renewals', 'Renewals'


class PaymentMethodChoices(models.TextChoices):
    CREDIT_CARD = 'credit_card', 'Credit Card'
    PAY_EASY = 'pay_easy', 'PayEasy'
    CONVENIENCE_STORE = 'convenience_store', 'Convenience Store'
