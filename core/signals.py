from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    """Send a short notification email to the user after a successful login.

    In development this will use the console email backend (prints to stdout).
    """
    if not getattr(user, 'email', None):
        # no email configured for this user; nothing to do
        return

    subject = 'Login successful'
    when = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S %Z')
    name = user.get_full_name() or user.username
    message = (
        f'Hello {name},\n\n'
        f'Your account successfully logged in on {when}.\n\n'
        "If this wasn't you, please reset your password or contact support.\n\n"
        'Regards,\nSahwira Team'
    )

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
    try:
        send_mail(subject, message, from_email, [user.email], fail_silently=False)
    except Exception:
        logger.exception('Failed to send login notification to %s', user.email)
