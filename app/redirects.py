from urlparse import urlparse
from urlparse import urljoin
from flask import request, url_for

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in (request.values.get('next'), request.referrer):
        if target and is_safe_url(target):
            return target
    return None
