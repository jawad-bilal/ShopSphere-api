import logging

from ..config import get_settings
from ..constants import PASSWORD_RESET_EXPIRE_MINUTES
from ..models import Order, User

logger = logging.getLogger(__name__)


def _send_email(to_email: str, subject: str, html: str) -> bool:
    settings = get_settings()
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY is not set; skipped email to %s", to_email)
        return False

    try:
        import resend

        resend.api_key = settings.resend_api_key
        resend.Emails.send(
            {
                "from": settings.resend_from_email,
                "to": [to_email],
                "subject": subject,
                "html": html,
            }
        )
        return True
    except Exception:
        logger.exception("Failed to send email to %s", to_email)
        return False


def send_password_reset_email(user: User, raw_token: str) -> bool:
    settings = get_settings()
    reset_url = f"{settings.frontend_url}/reset-password?token={raw_token}"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 560px; margin: 0 auto; color: #101828;">
      <h1 style="color: #2563eb;">ShopSphere</h1>
      <p>Hi {user.name},</p>
      <p>We received a request to reset your ShopSphere password.</p>
      <p>
        <a href="{reset_url}" style="display: inline-block; background: #2563eb; color: #fff; padding: 12px 18px; border-radius: 8px; text-decoration: none;">
          Reset password
        </a>
      </p>
      <p>This link expires in {PASSWORD_RESET_EXPIRE_MINUTES} minutes and can only be used once.</p>
      <p>If you did not request this, you can ignore this email. Your password will stay the same.</p>
      <p style="color: #667085; font-size: 13px;">For security, never share this link with anyone.</p>
    </div>
    """
    return _send_email(user.email, "Reset your ShopSphere password", html)


def send_order_confirmation_email(user: User, order: Order) -> bool:
    settings = get_settings()
    tracking_url = f"{settings.frontend_url}/order-success/{order.id}"
    item_rows = "".join(
        f"<tr><td style='padding:8px 0;'>{item.name}</td>"
        f"<td style='padding:8px 0; text-align:center;'>{item.quantity}</td>"
        f"<td style='padding:8px 0; text-align:right;'>${item.price:.2f}</td></tr>"
        for item in order.items
    )
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 560px; margin: 0 auto; color: #101828;">
      <h1 style="color: #2563eb;">ShopSphere</h1>
      <p>Hi {order.shipping_name},</p>
      <p>Thanks for your order. We have confirmed order <strong>#{order.id}</strong>.</p>
      <table style="width:100%; border-collapse: collapse;">{item_rows}</table>
      <p><strong>Total: ${order.total:.2f}</strong></p>
      <p>
        Ship to:<br/>
        {order.shipping_address}<br/>
        {order.shipping_city} {order.shipping_zip}
      </p>
      <p>
        <a href="{tracking_url}" style="display: inline-block; background: #2563eb; color: #fff; padding: 12px 18px; border-radius: 8px; text-decoration: none;">
          Track your order
        </a>
      </p>
    </div>
    """
    return _send_email(user.email, f"ShopSphere order #{order.id} confirmed", html)
