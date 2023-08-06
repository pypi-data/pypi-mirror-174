"""
Validates a URL or hostname

Takes a URL or hostname and validates by first parsing the input and
extracting the relevant fields. These are then individually checked
to ensure they are valid.

Typical Usage:
    >>> from urlprofiler.url.validator import validate_url
    >>> validate_url("https://google.com")
    "https://google.com"
"""

from urllib.parse import urlparse
import tldextract

class UrlException(Exception):
    """
    Exception for invalid URLs

    A custom exception that inherits from the exception base class. Raised
    when a URL does not pass validation.
    """
    pass

def validate_url(url):
    """
    Validates a URL 

    Takes a URL as input and validates by first parsing and then
    checking each individual component part of the URL.

    Args:
        url: URL to validate
    
    Returns:
        URL
    
    Raises:
        UrlException if URL is invalid
    """

    if not url.strip().startswith(('http://', 'https://')):
        raise UrlException(f"{url} should start with http or https")
    
    parsed_url = tldextract.extract(url)
    if not parsed_url.domain:
        raise UrlException(f"Domain name not found in {url}")
    
    if not parsed_url.suffix:
        raise UrlException(f"TLD not found in {url}")
    
    return url

class HostnameException(Exception):
    """
    Custom exception for invalid hostnames

    Raised when an invalid hostname is supplied to the validate_hostname
    method. Inherits from the Exception base class.
    """
    pass

def validate_hostname(hostname):
    """
    Validates a hostname

    Takes a hostname and validates to ensure it points to a (theoretically)
    real host. It parses the URL to fetch the domain name and the TLD, and
    returns the host name if these are valid.

    Args:
        hostname: host name to validate
    
    Returns:
        hostname if valid 
    
    Raises:
        HostnameException if invalid
    """

    parsed_host = tldextract.extract(hostname)
    
    if not parsed_host.domain:
        raise HostnameException(f"Domain name not found in {hostname}")
    
    if not parsed_host.suffix:
        raise HostnameException(f"TLD not found in {hostname}")
    
    hostname = ""
    
    if parsed_host.subdomain:
        hostname += f"{parsed_host.subdomain}."
    
    hostname += f"{parsed_host.domain}.{parsed_host.suffix}"
    
    return hostname

