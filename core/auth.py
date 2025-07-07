import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://leagues3.amsterdambilliards.com/team9ball/abc/login.php"
DASHBOARD_URL = "https://leagues3.amsterdambilliards.com/team9ball/abc/index.php"

def login(session: requests.Session, username: str, password: str):
    # First, perform GET to retrieve login page and hidden inputs
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract hidden inputs
    hidden_inputs = soup.find_all("input", type="hidden")
    form_data = {inp['name']: inp.get('value', '') for inp in hidden_inputs}

    # Add username and password
    form_data["user"] = username
    form_data["pwd"] = password
    form_data["action"] = "LOGIN"

    # Post login data
    login_response = session.post(LOGIN_URL, data=form_data)

    # Check if login was successful by checking for a known element on the dashboard
    if "Welcome Back to Team 9 Ball" not in login_response.text:
        return None, None

    return session, login_response.text
