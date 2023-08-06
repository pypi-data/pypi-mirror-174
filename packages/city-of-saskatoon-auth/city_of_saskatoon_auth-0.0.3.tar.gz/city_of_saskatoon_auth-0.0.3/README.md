# city-of-saskatoon-auth

An unofficial Python module for authenticating with the City of Saskatoon website.

Features:

1. Authenticates with both the main City of Saskatoon website/user portal
1. Authenticates with the My SmartUTIL tool
1. Provides a `requests.session` object that allows you to make authenticated requests
1. Allows saving and restoring your session for later use

## Usage

```python
from city_of_saskatoon_auth import session
s = session.Session('username', 'password')
s.login() # Log in to main City of Saskatoon portal
s.smart_util_login() # OPTIONAL: Log in to the My SmartUTIL portal

# You are now authenticated with the City of Saskatoon website, and can make authenticated requests.
# s.get() and s.post() are available, and use the same API as the requests library
s.get('URL')
s.post('URL', data={}, headers={})
```

## Saving and restoring your session

Your session can be written to a byte string that can either be saved to a file any other storage. It can then be later restored to make requests without logging in again.

WARNING: This archive contains your username and password, and is NOT secure. Be careful where you store it.

```python
from city_of_saskatoon_auth import session
s = session.Session('username', 'password')
s.login() # Log in to main City of Saskatoon portal

saved_session = s.to_archive()

s2 = session.Session.from_archive(saved_session)
s2.login() # Checks if the session is still valid, and logs in again if not
```

NOTE: Even though your main City of Saskatoon session was restored, you'll need to call `s.smart_util_login()` for every new session. This ensures you're getting the most up-to-date data.