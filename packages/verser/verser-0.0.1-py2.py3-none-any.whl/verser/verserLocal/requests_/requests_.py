from .ev_request import EVRequest

"""Request Class Instance"""
ev = EVRequest()

from rich import inspect


def get_request_with_cache(url):
    # ev = EVRequest()

    response = ev.get_request_by_checking_cache(url)
    print(url, "URL")

    return response
