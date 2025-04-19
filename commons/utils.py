"""

Taken from SmileyChris' post @ https://djangosnippets.org/snippets/690/

"""

import re

from django.utils.text import slugify

from django_currentuser.middleware import get_current_user as current_user


def unique_slugify(
    instance, value, slug_field_name="slug", queryset=None, slug_separator="-"
):
    """

    Calculates a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to

    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default

    to using the ``.all()`` queryset from the model's default manager.

    """

    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)

    slug_len = slug_field.max_length

    # Sort out the initial slug. Chop its length down if we need to.

    slug = slugify(value)

    if slug_len:
        slug = slug[:slug_len]

    slug = _slug_strip(slug, slug_separator)

    original_slug = slug

    # Create a queryset, excluding the current instance.

    if not queryset:

        # pylint: disable=W0212 # Access to a protected member _default_manager of a client class

        queryset = instance.__class__._default_manager.all()

        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again

    # (then '-3', etc).

    next = 2

    while not slug or queryset.filter(**{slug_field_name: slug}):

        slug = original_slug

        end = "-%s" % next

        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[: slug_len - len(end)]

            slug = _slug_strip(slug, slug_separator)

        slug = "%s%s" % (slug, end)

        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator=None):
    """

    Cleans up a slug by removing slug separator characters that occur at the

    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of

    the default '-' separator with the new separator.

    """

    if separator == "-" or not separator:

        re_sep = "-"

    else:

        re_sep = "(?:-|%s)" % re.escape(separator)

        value = re.sub("%s+" % re_sep, separator, value)

    return re.sub(r"^%s+|%s+$" % (re_sep, re_sep), "", value)


def get_current_user():
    return current_user


def get_updated_response_with_design_element(view, queryset, design_element):
    """

    returns the updated response for given queryset in a specific view

    this function will add design element in queryset response

    we need this kind of information (design_element) because of special request from phone team and

    we are keen on keeping the design control in backend

    """

    # checking if queryset or not

    # because at the very first login before assigning any roles under user account then the queryset

    # here we get will be empty ([]) and the paginate_queryset will raise exception while doing the count on empty list

    # so, instead of empty list the empty content queryset added as queryset

    if not queryset:
        from levelup.contents.models import Content

        queryset = Content.objects.none()

    page = view.paginate_queryset(queryset)

    if page is not None:
        ser = view.get_serializer(page, many=True)

        response = view.get_paginated_response(ser.data)

        # adding design element in paginated response

        response.data.update(design_element=design_element)

        return response.data

    ser = view.get_serializer(queryset, many=True)

    response = dict(data=ser.data, **design_element)

    return response


def is_mobile_user(request):
    # TODO: Dipesh, add extra checks to make sure that the request is coming from mobile

    from django.conf import settings

    headers = settings.APP_HEADER_INFORMATION

    app_name = headers.get("APP_NAME")

    app_version = headers.get("APP_VERSION")

    if request.headers.get(app_name) and request.headers.get(app_version):
        return True


def get_file_type(file):
    ext = file.split(".")[1]

    if ext in ["pdf"]:
        return "PDF"

    if ext in ["docx", "doc", "txt"]:
        return "DOCUMENT"

    if ext in ["xlsx", "xls"]:
        return "EXCEL"

    if ext in ["csv"]:
        return "CSV"

    if ext in ["jpg", "png", "jpeg", "svg"]:
        return "IMAGE"

    return None
