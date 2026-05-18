from .models import AuditLog


def log_audit(request, action, description, model_name=None, object_id=None, status='success'):
    """Log user action for audit trail"""
    try:
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500] if hasattr(request, 'META') else ''

        AuditLog.objects.create(
            user=user,
            action=action,
            description=description,
            model_name=model_name,
            object_id=object_id,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to log audit: {e}")


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip or '0.0.0.0'
