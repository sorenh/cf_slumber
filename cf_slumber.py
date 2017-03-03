import slumber
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

class CloudFoundrySlumberClient(slumber.API):
    def __init__(self, username, password, endpoint="https://api.run.pivotal.io/v2/"):
        session = OAuth2Session(client=LegacyApplicationClient(client_id="cf"))
        super(CloudFoundrySlumberClient, self).__init__(endpoint, append_slash=False, session=session)
        session.fetch_token(token_url=self._auth_token_url(),
                            username=username,
                            password=password,
                            client_id='cf')

    def _auth_token_url(self):
        cf_info = self.info.get()
        return '%s/oauth/token' % (cf_info['authorization_endpoint'],)