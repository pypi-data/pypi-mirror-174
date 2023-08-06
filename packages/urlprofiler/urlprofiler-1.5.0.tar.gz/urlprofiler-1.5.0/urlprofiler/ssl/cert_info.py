"""
Extracts data from SSL certificates

Fetches relevant data from SSL certificates. It includes the name of the
issuer, along with available organisational information.

Typical Usage:
    >>> from urlprofiler.ssl.cert_info import get_cert_info
    >>> get_cert_info()
    '{....}'
"""

import ssl
import socket
import certifi
import itertools
from urllib.parse import urlparse
from warnings import warn

from urlprofiler.url.validator import validate_hostname

class CertInfo:
    """
    Fetches various datapoints from a hostname

    Contains various methods that fetch additional data about a URL. This 
    module requires a hostname, which is validated, and tries to fetch the
    SSL certificate for that URL.  It also extracts the IP address of the
    host server.

    Attributes:
        hostname: name of host to connect to
    """

    def __init__(self, hostname):
        """
        Constructor for CertInfo object

        Takes a hostname and assigns as an instance variable. Then validates 
        to ensure it is accurate.

        Args:
            hostname: name of host to connect to
        
        Returns:
            None
        
        Raises:
            None
        """

        self.hostname = validate_hostname(hostname)
    
    def get_ssl_info(self):
        """
        Fetches SSL certificate information for host

        Gets and returns SSL certificate information for a host, if such 
        information is available. Data including the name of the issuer
        and the expiry date are provided within a dictionary.

        Args:
            None
        
        Returns: 
            Dictionary of SSL related data e.g.,:

            {
                "issuer": "DigiCert"
                "expiryDate": 1900-01-01T00:00:00
            }
        
        Raises:
            None
        """

        context = ssl.create_default_context(cafile=certifi.where())
        with context.wrap_socket(socket.socket(), server_hostname=self.hostname) as _socket:
            
            try:
                _socket.connect((self.hostname, 443))
            except ssl.SSLCertVerificationError as cert_err:
                print("SSL certificate verification failed. Do you have certifi installed?")
            
            cert = _socket.getpeercert()
        
        cert_info = {}
        for key, value in cert.items():    

            if not isinstance(value, tuple):
                cert_info[key] = value
                continue
            
            elif not isinstance(value[0], tuple):
                cert_info[key] = value[0]
                continue

            elif isinstance(value[0], tuple) and len(value) == 1:
                cert_info[key] = dict(itertools.chain.from_iterable(value))
                continue

            elif value[0][0] == "DNS":
                dns_data = []
                for dns_name in value:
                    dns_data.append(dns_name[1])
                cert_info["dns"] = dns_data
                continue
            
            cert_info[key] = {a:b for a, b in sum(value, ())}
        
        return cert_info
    
    def get_ip_address(self, hostname=None):
        """
        Fetches and return the IP address of server

        Resolves the IP address of the host machine that a given hostname
        is running on. Note this is the IP address of the server, which may
        not bear any relation to the actual company behind the hostname.

        Args:
            hostname: defaults to hostname provided in constructor
        
        Returns
            None
        
        Raises:
            None
        """

        if not hostname: 
            hostname = self.hostname

        ip_address = None
        
        try:
            ip_address = socket.gethostbyname(self.hostname)
        except Exception as exception:
            exception_name = exception.__class__.__name__
            warn(f"Unable to get server IP address due to {exception_name} error")
        
        return {"Server IP": ip_address}
