import urllib
import urllib2

class TequilaClient(object): 
    def __init__(self, config):
        self.config = config
        
        self.is_authenticated = False
        self.request_key = None

    def _open_url(self, url, data = None, additional_values = ""):
        """ hide urllib2 access, return header and response """
        url_values = None
        
        if data:
            url_values = urllib.urlencode(data)
        if url_values:
            url + "?" + url_values
            req = urllib2.Request(url + "?" + url_values + additional_values)
        else:
            req = urllib2.Request(url)

#        try:
        response = urllib2.urlopen(req)
#        except HTTPError, e:
#        except URLError, e:
        return response.read()
    
    def _get_key(self):
        """ hide urllib2 access """
        if self.request_key:
            return self.request_key
        
        if self.config.request:
            list_request = ""
        
            for request in self.config.request:
                if list_request:
                    list_request += "+" 
                
                list_request += request
        else:
            raise ValueError("username attribute is mandatory in request")
       
        params = {'urlacces' : self.config.redirect_to,
                  'service' : self.config.service,
                  'allows' : self.config.allows
                 }
        
        if self.config.additional_params:
            params.update(self.config.additional_params)
        
        self.request_key = self._open_url(self.config.server_url + "/cgi-bin/tequila/createrequest", params, "&request=" + list_request)[4:-1]
        
        return self.request_key

    key = property(_get_key)
    
    def login_url(self):
        return self.config.server_url + "/cgi-bin/tequila/auth?requestkey=" + self.key

    def get_attributes(self, key = None):
        """ return a dictionnary of attributes setted by tequila,
            corresponding with the "request" parameter in config
         """
        if key:
            params = {'key' : key}
        elif self.request_key:
            params = {'key' : self._get_key()}
        else:
            raise ValueError()
        
        response = self._open_url(self.config.server_url + "/cgi-bin/tequila/fetchattributes", params)
        
        attributes = {}
        list_attributes = response.split('\n')
        
        for attribute in list_attributes[:-1]:
            splitted_attr = attribute.split('=')
            attributes[splitted_attr[0]] = splitted_attr[1]
            
        if not self._verify_attributes(attributes):
            raise StandardError()
        
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