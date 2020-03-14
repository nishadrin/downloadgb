from common.config import MAIN_LINK


class AuthorizationGeekBrains:
    """Connect to GeekBrains with login and password."""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def get_token(self):
        """Get authenticity data."""
        self.url = f"{MAIN_LINK}login"
        self.connect = requests.Session()
        self.html = self.connect.get(self.url,verify=True)
        self.soup = BeautifulSoup(self.html.content, "html.parser")
        self.hidden_auth_token = self.soup.find(
            'input', {'name': 'authenticity_token'})['value']

    def authorization(self):
        """Authorize to GeekBrains."""
        self.connect.get(self.url, verify=True)
        self.login_data = {
            "utf8": "✓", "authenticity_token": self.hidden_auth_token,
            "user[email]": self.email, "user[password]": self.password,
            "user[remember_me]": "0"
            }
        self.connect.post(
            MAIN_URL,
            data=self.login_data,
            headers={"Referer": f"{MAIN_LINK}login"}
            )

    def login_gb(self):
        """Login to GeekBrains."""
        self.get_token()
        self.authorization()

    def logout_gb(self):
        """Logout."""
        self.connect.close()
