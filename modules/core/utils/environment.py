from django.conf import settings


def get_admin_environment(request):
    """
    Callback returns a list of two values:
    [ "Text Label", "color_type" ]
    Available color types: 'success' (green), 'danger' (red), 'warning' (orange), 'info' (blue)
    """
    if settings.DEBUG:
        return ["DEVELOPMENT", "success"]  # Renders a green badge

    return ["PRODUCTION", "danger"]  # Renders a red badge
