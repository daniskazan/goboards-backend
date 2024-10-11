import urllib.parse

from configs.oauth.vk import VKOauthConfig


class VKRedirectLinkProvider:
    def __init__(self):
        self._client_id = VKOauthConfig.VK_CLIENT_ID
        self._redirect_uri = VKOauthConfig.VK_REDIRECT_URI
        self._authorize_url = VKOauthConfig.VK_AUTHORIZE_URL
        self._response_type = VKOauthConfig.VK_RESPONSE_TYPE

    @property
    def redirect_link(self) -> str:
        params = {
            "client_id": self._client_id,
            "display": "page",
            "redirect_uri": self._redirect_uri,
            "response_type": self._response_type,
        }
        link = self._authorize_url + urllib.parse.urlencode(params)
        return link
