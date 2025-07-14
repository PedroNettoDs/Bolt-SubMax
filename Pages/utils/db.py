from django.db import OperationalError


def safe_all(model):
    """Return all objects of a model or an empty queryset if unavailable."""
    try:
        return model.objects.all()
    except OperationalError:
        return model.objects.none()


def safe_count(obj_or_qs):
    """Return count of queryset or model, handling missing tables."""
    try:
        if hasattr(obj_or_qs, 'count'):
            return obj_or_qs.count()
        return obj_or_qs.objects.count()
    except OperationalError:
        return 0
