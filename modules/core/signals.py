import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

logger = logging.getLogger(__name__)


def send_password_setup_email(user):
    path = reverse(
        "password_reset_confirm",
        kwargs={
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )

    context = {"user": user, "setup_url": f"{settings.SITE_URL}{path}"}

    try:
        email = EmailMultiAlternatives(
            "Welcome - set up your account",
            render_to_string("email/password_setup.txt", context),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        email.attach_alternative(
            render_to_string("email/password_setup.html", context), "text/html"
        )
        email.send()
    except Exception:
        logger.exception("Could not send password setup email for user %s", user.pk)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def email_new_user_password_setup(sender, instance, created, **kwargs):
    if created and instance.email:
        transaction.on_commit(lambda: send_password_setup_email(instance))
