from django.db.models import QuerySet


def queryset_to_list(queryset: QuerySet, field_name: str):
    """
    Convert the given QuerySet to a list by extracting values from the specified field.

    Args:
        queryset (QuerySet): Queryset to be converted to a list.
        field_name (str): Name of the field to extract values from.

    Returns:
        list: List containing values extracted from the specified field.
    """
    return list(queryset.values_list(field_name, flat=True))
