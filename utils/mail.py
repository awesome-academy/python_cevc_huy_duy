from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from constants.email_templates import EmailTemplates, EmailSubjects

def send_confirmation_email(user, request):
    try:
        confirmation_url = request.build_absolute_uri(
            reverse('email-confirm') + f'?token={user.confirmation_token}'
        )

        message = EmailTemplates.account_confirmation(
            user_name=f"{user.first_name} {user.last_name}",
            confirmation_url=confirmation_url
        )

        send_mail(
            subject=EmailSubjects.ACCOUNT_CONFIRMATION,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending confirmation email: {e}")