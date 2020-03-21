import requests
from bs4 import BeautifulSoup

from common.config import MAIN_LINK


class AuthorizationGeekBrains:
    """Connect to GeekBrains with login and password."""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def get_token(self):
        """Get authenticity data."""
        self.url = f"{MAIN_LINK}/login"
        self.connect = requests.Session()
        self.html = self.connect.get(self.url,verify=True)
        self.soup = BeautifulSoup(self.html.content, "html.parser")
        print(self.soup)
        self.hidden_auth_token = self.soup.find(
            'input', {'name': 'authenticity_token'})['value']
        print(self.hidden_auth_token)

    def authorization(self):
        """Authorize to GeekBrains."""
        self.connect.get(self.url, verify=True)
        self.login_data = {
            "utf8": "✓", "authenticity_token": self.hidden_auth_token,
            "user[email]": self.email, "user[password]": self.password,
            "user[remember_me]": "0"
            }
        self.connect.post(
            MAIN_LINK,
            data=self.login_data,
            headers={"Referer": f"{self.url}"}
            )

    def login_gb(self):
        """Login to GeekBrains."""
        try:
            self.get_token()
            self.authorization()
        except ConnectionError:
            raise ConnectionError

    def logout_gb(self):
        """Logout."""
        self.connect.close()


class Parser(AuthorizationGeekBrains):

    def get_soup(self, url: str) -> BeautifulSoup:
        """Get lesson's BeautifulSoup."""
        try:
            html = self.connect.get(url)
        except ConnectionError:
            return None

        return BeautifulSoup(html.content, "html.parser")
