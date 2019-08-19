"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

import json
import logging
import sys
import urllib

from django.utils.encoding import smart_str

logger = logging.getLogger('django_tequila.client')


try:
    # For Python 2
    from urllib2 import Request
except ImportError:
    # For Python 3
    from urllib.request import Request

try:
    # For Python 2
    url_encoding_method = urllib.urlencode
except AttributeError:
    # For Python 3
    url_encoding_method = urllib.parse.urlencode

try:
    # For Python 2
    from urllib2 import urlopen
except ImportError:
    # For Python 3
    from urllib.request import urlopen


class TequilaClient(object):
    def __init__(self, config):
        self.config = config

        self.is_authenticated = False
        self.request_key = None

    def _open_url(self, url, data=None, additional_values=""):
        """ hide urllib2 access, return header and response """
        url_values = None

        if data:
            url_values = url_encoding_method(data)
        if url_values:
            final_url = url + "?" + url_values + additional_values
        else:
            final_url = url

        req = Request(final_url)

        # TODO: try..except HTTPError or URLError
        logger.debug("Opening url %s , ..." % final_url)
        response = urlopen(req)

        return response.read()

    def _get_key(self):
        """ hide urllib2 access """
        logger.debug("Asking for a key...")

        if self.request_key:
            logger.debug("Key already loaded...")
            return self.request_key

        logger.debug("No key found, fetching a new one...")

        if self.config.request:
            list_request = '+'.join(self.config.request)
        else:
            raise ValueError("username attribute is mandatory in request")

        params = {'urlacces': smart_str(self.config.redirect_to),
                  'service': self.config.service,
                  'allows': self.config.allows
                  }

        if self.config.additional_params:
            params.update(self.config.additional_params)

        self.request_key = self._open_url(
            self.config.server_url + "/cgi-bin/tequila/createrequest", params,
            "&request=" + list_request)[4:-1]

        logger.debug("Key generated : %s " % self.request_key)

        return self.request_key

    key = property(_get_key)

    def login_url(self):

        if sys.version_info < (3,):
            key = self.key
        else:
            key = self.key.decode('UTF-8')
        return self.config.server_url + "/cgi-bin/tequila/auth?requestkey=" + key

    def get_attributes(self, key=None, allowedrequesthosts=None):
        """ return a dictionnary of attributes setted by tequila,
            corresponding with the "request" parameter in config
         """
        logger.debug("Asking for attributes...")

        if key:
            params = {'key': key}
        elif self.request_key:
            params = {'key': self._get_key()}
        else:
            raise ValueError()

        if allowedrequesthosts:
            params['allowedrequesthosts'] = allowedrequesthosts

        response = self._open_url(
            self.config.server_url + "/cgi-bin/tequila/fetchattributes",
            params)

        attributes = {}

        # force utf-8 as django need it
        response = response.decode('utf-8')

        list_attributes = response.split('\n')

        logger.debug(
            "Attributes returned by %s : \n%s" % (self.config.server_url,
                                                  json.dumps(list_attributes,
                                                             sort_keys=True,
                                                             indent=4)))

        for attribute in list_attributes[:-1]:
            splitted_attr = attribute.split('=')

            if len(splitted_attr) == 1:
                splitted_attr.append('')

            attributes[splitted_attr[0]] = splitted_attr[1]

        if not self._verify_attributes(attributes):
            raise ValueError("Some Attributes returned by Tequila are missing")

        logger.debug(
            "Attributes after formatting and returned: \n%s" % json.dumps(
                attributes,
                sort_keys=True, indent=4))

        return attributes

    def _verify_attributes(self, attributes):
        needed_attrs = ['org', 'user', 'host', 'key']

        for needed_attribute in needed_attrs:
            try:
                if not attributes[needed_attribute]:
                    return False
            except KeyError:
                return False
        return True
