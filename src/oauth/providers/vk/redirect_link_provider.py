import urllib.parse

from configs.oauth import oauth


class VKRedirectLinkProvider:
    client_id = oauth.VK_CLIENT_ID
    redirect_uri = oauth.VK_REDIRECT_URI
    response_type = oauth.VK_RESPONSE_TYPE

    @property
    def redirect_link(self) -> str:
        params = {
            "client_id": self.client_id,
            "display": "page",
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
        }
        link = oauth.VK_AUTHORIZE_URL + urllib.parse.urlencode(params)
        return link
