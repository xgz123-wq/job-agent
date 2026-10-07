"""Client email template service

Send verification codes and other emails using SMTP.
"""
from app.core.config import settings
from app.services.common.email_smtp import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
)


class ClientEmailService:
    @staticmethod
    async def send_registration_verification(email: str, verification_code: str, user_name: str = None):
        """Send registration verification code email"""
        await send_verification_email(
            email=email,
            verification_code=verification_code,
            first_name=user_name or "User",
            expires_minutes=10,
        )

    @staticmethod
    async def send_password_reset_code(email: str, verification_code: str, user_name: str = None):
        """Send password reset verification code email"""
        await send_password_reset_email(
            email=email,
            verification_code=verification_code,
            first_name=user_name or "User",
            expires_minutes=10,
        )

    @staticmethod
    async def send_welcome(email: str, user_name: str = None, dashboard_url: str = None):
        """Send welcome email

        Args:
            email: Recipient email
            user_name: User name
            dashboard_url: Dashboard URL; defaults to ``{settings.FRONTEND_URL}/dashboard``
        """
        url = dashboard_url or f"{settings.FRONTEND_URL}/dashboard"
        await send_welcome_email(
            email=email,
            first_name=user_name or "User",
            dashboard_url=url,
        )


client_email_service = ClientEmailService()
