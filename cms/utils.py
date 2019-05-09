import re
import os
from uuid import uuid4
from django.db.models import Q
from django.db.models.sql.query import get_order_dir
from django.utils.translation import get_language

def i18n_grep(text):
    i18n_values = re.findall('<!--\s*([a-zA-Z]+)\s*-->\n*((?:(?!<!--\s*[a-zA-Z]+\s*-->).)*)', text)

    if not i18n_values:
        return text

    lang_code = get_language()

    for translation in i18n_values:
        if lang_code == translation[0]:
            return translation[1]

    return text

def hide_first_item(text):
    items = re.search('(<p>)?((<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>))(</p>)?', text)
    if items:
        item = items.group(0)
        text = text.replace(item, '')
    return text

def get_post_announce(item):
    text = item.text

    items = re.search('(<img[^>]+>)|(<iframe[^>]+>[^<]*</iframe>)', text)
    if items:
        return items.group(0)

    return ''

def get_next_or_previous(qs, item, next=True):
    """
    Get the next or previous object in the queryset, with regards to the
    item specified.
    """
    # If we want the previous object, reverse the default ordering
    if next:
        default_ordering = 'ASC'
    else:
        default_ordering = 'DESC'

    # First, determine the ordering. This code is from get_ordering() in
    # django.db.sql.compiler
    if qs.query.extra_order_by:
        ordering = qs.query.extra_order_by
    elif not qs.query.default_ordering:
        ordering = qs.query.order_by
    else:
        ordering = qs.query.order_by or qs.query.model._meta.ordering

    assert not ordering == '?', 'This makes no sense for random ordering.'

    query_filter = None
    for field in ordering:
        item_value = getattr(item, field)

        # Account for possible reverse ordering
        field, direction = get_order_dir(field, default_ordering)

        # Either make sure we filter increased values or lesser values
        # depending on the sort order
        if direction == 'ASC':
            filter_dict = {'%s__gt' % field: item_value}
        else:
            filter_dict = {'%s__lt' % field: item_value}

        # Make sure we nicely or the conditions for the queryset
        if query_filter:
            query_filter = query_filter | Q(**filter_dict)
        else:
            query_filter = Q(**filter_dict)

    # Reverse the order if we're looking for previous items
    if default_ordering == 'DESC':
        qs = qs.reverse()

    # Filter the queryset
    qs = qs.filter(query_filter)

    # Return either the next/previous item or None if not existent
    try:
        return qs[0]
    except IndexError:
        return None

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)

    return wrapper