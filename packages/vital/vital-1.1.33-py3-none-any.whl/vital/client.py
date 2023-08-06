import requests

from vital.api import (
    Activity,
    Body,
    Devices,
    Link,
    Profile,
    Sleep,
    Testkits,
    User,
    Vitals,
    Webhooks,
    Workouts,
)
from vital.internal.requester import (
    DEFAULT_TIMEOUT,
    delete_request,
    get_request,
    post_request,
)
from vital.internal.token_handler import TokenHandler
from vital.internal.utils import urljoin

base_urls = {
    "eu": {
        "prod": "https://api.eu.tryvital.io",
        "production": "https://api.eu.tryvital.io",
        "dev": "https://api.dev.eu.tryvital.io",
        "sandbox": "https://api.sandbox.eu.tryvital.io",
    },
    "us": {
        "prod": "https://api.tryvital.io",
        "production": "https://api.tryvital.io",
        "dev": "https://api.dev.tryvital.io",
        "sandbox": "https://api.sandbox.tryvital.io",
    },
}


def get_base_url(environment: str, region: str) -> str:
    if environment == "local":
        return "http://localhost:8000"
    try:
        return base_urls[region][environment]
    except KeyError:
        raise Exception("Environment not supported")


class Client:
    """
    Python Vital API client.
    All of the endpoints documented under the ``vital.api``
    module may be called from a ``vital.Client`` instance.
    """

    def __init__(
        self,
        client_id=None,
        secret=None,
        environment=None,
        timeout=DEFAULT_TIMEOUT,
        api_version="v2",
        region="us",
        api_key=None,
        **kwargs,
    ):
        """
        Initialize a client with credentials.
        :param  str     client_id:          Your Vital client ID
        :arg    str     secret:             Your Vital secret
        :arg    str     environment:        One of ``sandbox`` or ``production``.
        :arg    int     timeout:            Timeout for API requests.
        :arg    str     api_key:            Your Vital api key - can be used to
            replace client ID and secret.
        """
        self.client_id = client_id
        self.client_secret = secret
        self.environment = environment
        self.timeout = timeout
        self.api_version = api_version
        self.base_url = get_base_url(environment, region)
        self.api_key = api_key
        self.headers = {
            "Accept-Encoding": "deflate",
        }
        if self.api_key:
            self.headers["x-vital-api-key"] = self.api_key
        else:
            self.token_handler = TokenHandler(
                self.client_id,
                self.client_secret,
                self.environment,
                audience=kwargs.get("audience"),
                domain=kwargs.get("domain"),
            )
            self.headers["Authorization"] = f"Bearer {self.token_handler.access_token}"
        self.session = requests.Session()
        # Mirror the HTTP API hierarchy
        self.Profile = Profile(self)
        self.Link = Link(self)
        self.Body = Body(self)
        self.Activity = Activity(self)
        self.Sleep = Sleep(self)
        self.User = User(self)
        self.Workouts = Workouts(self)
        self.Webhooks = Webhooks(self)
        self.Vitals = Vitals(self)
        self.Testkits = Testkits(self)
        self.Devices = Devices(self)

    def post(
        self, path, data=None, is_json=True, params={}, headers={}, api_version=None
    ):
        """Make a post request."""
        return self._post(
            path, data, is_json, params, self.session, headers, api_version
        )

    def get(self, path, params={}, headers={}, api_version=None):
        """Make a get request."""
        return self._get(path, params, self.session, headers, api_version)

    def delete(self, path, params={}, api_version=None):
        """Make a delete request."""
        return self._delete(path, params, self.session, api_version)

    def post_public(self, path, data, is_json=True, api_version=None):
        """Make a post request requiring no auth."""
        return self._post(path, data, is_json, self.session, api_version)

    def _post(
        self, path, data, is_json, params={}, session=None, headers={}, api_version=None
    ):
        headers = {
            **self.headers,
            **headers,
        }
        return post_request(
            urljoin(
                self.base_url,
                f"{self.api_version if not api_version else api_version}{path}",
            ),
            data=data,
            timeout=self.timeout,
            is_json=is_json,
            headers=headers,
            params=params,
            session=session,
        )

    def _get(self, path, params={}, session=None, headers={}, api_version=None):
        headers = {
            **self.headers,
            **headers,
        }
        return get_request(
            urljoin(
                self.base_url,
                f"{self.api_version if not api_version else api_version}{path}",
            ),
            timeout=self.timeout,
            headers=headers,
            params=params,
            session=session,
        )

    def _delete(self, path, params={}, session=None, api_version=None):
        headers = {
            **self.headers,
        }
        return delete_request(
            urljoin(
                self.base_url,
                f"{self.api_version if not api_version else api_version}{path}",
            ),
            timeout=self.timeout,
            headers=headers,
            params=params,
            session=session,
        )
