from django import template
from django.http import QueryDict

from urllib.parse import urlsplit, urlunsplit
from index.models import *

register = template.Library()


@register.simple_tag(takes_context=True)
def update_query_params(context, url=None, **kwargs):
    if url is None:
        url_before = context['request'].get_full_path()
    else:
        url_before = url
    url_after = _update_query_params(url_before, **kwargs)
    return url_after

def _update_query_params(url_before: str, **kwargs) -> str:
    scheme, netloc, path, query_before, fragment = urlsplit(url_before)
    query_dict = QueryDict(query_before, mutable=True)
    # на query_dict.update() не менять, иначе будет ?page=1&page=2
    for k, v in kwargs.items():
        query_dict[k] = v
    query_after = query_dict.urlencode()
    url_after = urlunsplit((scheme, netloc, path, query_after, fragment))
    return url_after


@register.filter(name='number_of_patients')
def number_of_patients(user):
    return sum([(user.count_sender or 0),
                (user.count_founder or 0), 
                (user.count_both or 0)])