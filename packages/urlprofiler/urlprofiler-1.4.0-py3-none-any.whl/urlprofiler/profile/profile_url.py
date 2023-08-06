"""
Returns relavant metadata about a URL

Fetches various data points about a URL and returns within a dictionary, including
connection details (status code, redirect history, connection latency) and SSL 
information (issuer, expiry date, IP address). This does not print results to the 
console; it simply returns the data.

Typical Usage:

>>> from urlprofiler.profile.profile_url import profile_url
>>> profile_url("google.com")
{....}
"""

import sys

from urlprofiler.http.request import Request
from urlprofiler.ssl.cert_info import CertInfo

def profile_url(url):
    """
    Profiles a URL and returns relevant metadata

    Takes a URL and runs through a number of methods to extract various
    pieces of metadata, including the HTTP status code, SSL certificate
    information and IP address data. 

    Args:
        url: URL to profile
    
    Returns:
        Dictionary of URL metadata e.g.,
        {
            "status_code": 200
            "latency (seconds)": 0.345
        }
    
    Raises:
        None
    """

    if not url.strip().startswith(("http://", "https://")):
        url = f"http://{url}"
    
    url_info = {"url": url}

    http_connection = Request(url)
    
    url_info.update(http_connection.get_status_code())
    url_info.update(http_connection.track_url())
    url_info.update(http_connection.get_connection_data())


    cert_info = CertInfo(url_info["end_url"])
    if url_info["end_url"].startswith("https"):
        url_info.update(cert_info.get_ssl_info())
    
    url_info.update(cert_info.get_ip_address())

    return url_info


def profile_url_cli():
    """
    Implements profile_url with command line args

    Instantiates profile_url() and fetches a value from the command line via
    argv. If no arguments are found via argv, an error message is printed.
    Otherwise, profile_url() is executed and the resut pretty printed to the
    terminal.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        None
    """

    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: urlprofiler https://example.com")
    
    for arg in args:
        profile = profile_url(arg)
        print(profile)
