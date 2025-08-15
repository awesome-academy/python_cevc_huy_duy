# =============================================================================
# Email Subjects
# =============================================================================

class EmailSubjects:
    ACCOUNT_CONFIRMATION = "Account Verification - Co-Working Space"


# =============================================================================
# Email Templates
# =============================================================================

class EmailTemplates:
    @staticmethod
    def account_confirmation(user_name, confirmation_url):
        return f"""
        Hello {user_name},
        
        Thank you for registering an account at Co-Working Space Booking System.
        
        To complete the registration process, please click the link below to verify your email:
        
        {confirmation_url}
        
        If you did not create this account, please ignore this email.
        
        Best regards,
        Co-Working Space Team
        """
