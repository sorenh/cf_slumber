import unittest
import requests_mock

import six.moves.urllib.parse as urlparse

from cf_slumber import CloudFoundrySlumberClient

class CloudFoundrySlumberClientTestCase(unittest.TestCase):
    orgs = {"total_results": 1,
            "total_pages": 1,
            "prev_url": None,
            "next_url": None,
            "resources": [
               {
                  "metadata": {
                     "guid": "f51a794d-5f49-411d-ac2a-22c5b001e787",
                     "url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787",
                     "created_at": "2017-02-08T08:24:58Z",
                     "updated_at": "2017-02-08T08:27:47Z"
                  },
                  "entity": {
                     "name": "soren-org",
                     "billing_enabled": True,
                     "quota_definition_guid": "7dbdcbb7-edb6-4246-a217-2031a75388f7",
                     "status": "active",
                     "default_isolation_segment_guid": None,
                     "quota_definition_url": "/v2/quota_definitions/7dbdcbb7-edb6-4246-a217-2031a75388f7",
                     "spaces_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/spaces",
                     "domains_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/domains",
                     "private_domains_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/private_domains",
                     "users_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/users",
                     "managers_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/managers",
                     "billing_managers_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/billing_managers",
                     "auditors_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/auditors",
                     "app_events_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/app_events",
                     "space_quota_definitions_url": "/v2/organizations/f51a794d-5f49-411d-ac2a-22c5b001e787/space_quota_definitions"
                  }
               }
             ]
           }

    @requests_mock.Mocker()
    def test_auth(self, m):
        m.register_uri('GET', 'https://api.run.pivotal.io/v2/info',
                       headers={'Content-Type': 'application/json'},
                       json={"name": "",
                             "build": "",
                             "support": "https://support.run.pivotal.io",
                             "version": 0,
                             "description": "Cloud Foundry sponsored by Pivotal",
                             "authorization_endpoint": "https://login.run.pivotal.io",
                             "token_endpoint": "https://login.run.pivotal.io",
                             "min_cli_version": "6.22.0",
                             "min_recommended_cli_version": "latest",
                             "api_version": "2.75.0",
                             "app_ssh_endpoint": "ssh.run.pivotal.io:2222",
                             "app_ssh_host_key_fingerprint": "e7:13:4e:32:ee:39:62:df:54:41:d7:f7:8b:b2:a7:6b",
                             "app_ssh_oauth_client": "ssh-proxy",
                             "routing_endpoint": "https://api.run.pivotal.io/routing",
                             "logging_endpoint": "wss://loggregator.run.pivotal.io:443",
                             "doppler_logging_endpoint": "wss://doppler.run.pivotal.io:443"})
        m.register_uri('POST', 'https://login.run.pivotal.io/oauth/token',
                       headers={'Content-Type': 'application/json'},
                       json={"access_token":
                             "642538552532564752386475123847651475128647523671253425485675uyg23k3jh5glekjrsfsqwerh",
                             "token_type": "bearer",
                             "refresh_token": "2376454825381623796745987659813725485763924162548523984616492486729846729",
                             "expires_in": 599,
                             "scope": "openid uaa.user cloud_controller.read password.write cloud_controller.write",
                             "jti": "45185562334324444444444444112ef0"})
        m.register_uri('GET', 'https://api.run.pivotal.io/v2/organizations',
                       headers={'Content-Type': 'application/json'},
                       json=self.orgs)

        cf = CloudFoundrySlumberClient('theusername', 'thepassword')

        orgs = cf.organizations.get()

        self.assertEquals(len(m.request_history), 3)

        self.assertEquals(urlparse.parse_qs(m.request_history[1].text),
                          {'client_id': ['cf'],
                           'grant_type': ['password'],
                           'password': ['thepassword'],
                           'username': ['theusername']})
        self.assertEquals(orgs, self.orgs)
