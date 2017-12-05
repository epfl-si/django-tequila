"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""


class Config(object):
    def __init__(self,
                 server_url,
                 additional_params=None,
                 redirect_to=None,
                 service=None,
                 request=None,
                 language=None,
                 localserver=None,
                 org=None,
                 langage=None,
                 want_right=None,
                 want_role=None,
                 allows=None,
                 strong_authentication=False
                 ):

        self.server_url = server_url

        if redirect_to:
            if redirect_to.find('http://') == -1 and redirect_to.find('https://') == -1:
                self.redirect_to = 'https://' + redirect_to
            else:
                self.redirect_to = redirect_to
        else:
            self.redirect_to = None

        self.additional_params = additional_params

        if strong_authentication:
            strong_authentication_param = {'authstrength': 3}

            if self.additional_params:
                self.additional_params.update(strong_authentication_param)
            else:
                self.additional_params = strong_authentication_param

        self.service = service
        self.request = request
        self.langage = langage or "english"
        self.allows = allows


class EPFLConfig(Config):
    """ Specific config currently used @ EPFL
    More info on config options https://tequila.epfl.ch/info """

    def __init__(self, allow_guests=False, *args, **kwargs):
        if not kwargs.get('server_url'):
            kwargs['server_url'] = "https://tequila.epfl.ch"

        super(EPFLConfig, self).__init__(*args, **kwargs)

        if not kwargs.get('org'):
            self.org = "EPFL"

        if not kwargs.get('request'):
            self.request = ["name",
                            "firstname",
                            "statut",
                            "username",
                            "classe",
                            "uniqueid",
                            "email",
                            "allunits",
                            "where",
                            "group",
                            "memberof"]

        if allow_guests:
            self.allow_guests()

    def allow_guests(self):
        """ Use preventive config, by default, set guests as 'not allowed' """
        if self.allows:
            self.allows += '|categorie=epfl-guests'
        else:
            self.allows = 'categorie=epfl-guests'
