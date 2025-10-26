import json
import os
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from datetime import datetime, UTC


"""
A module to support authentication and authorization
with the Auth0 service provider.
"""

"""
Auth0 related configuration
provided externally with environment variables.
"""
AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
AUTH0_AUDIENCE = os.environ["AUTH0_AUDIENCE"]

# The following settings default to local development
# whem not explicitly set in environment variables
AUTH0_CALLBACK_SCHEME = os.environ.get("AUTH0_CALLBACK_SCHEME", "http")
AUTH0_CALLBACK_SERVER = os.environ.get(
    "AUTH0_CALLBACK_SERVER", "127.0.0.1:5000"
)


ALGORITHMS = ["RS256"]


"""
For testing we enable to deactivate authentication and
authorization using an environment variable.

For safe production use authentication and authorization
is always activated unless explicitly deactivated.
"""
AUTH_DEACTIVATED = "AUTH_DEACTIVATED"
_auth_explicitly_deactivated = False


def disable_auth_checks_explicitly_for_testing(disable: bool):
    global _auth_explicitly_deactivated
    _auth_explicitly_deactivated = disable


"""
Enable to explicitly use environment variable
to deactivate auth for testing purposes in an
environment.
"""
if os.environ.get(AUTH_DEACTIVATED, "False").lower() == "true":
    warning_message = """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!! WARNING: NON-PRODUCTION USE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !! Authentication and authorization checks have been disabled!!!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """.strip(" \t")
    print(warning_message)
    disable_auth_checks_explicitly_for_testing(True)


def is_auth_explicitly_deactivated():
    return _auth_explicitly_deactivated


"""
AuthError Exception
A standardized way to communicate auth failure modes
"""


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header.

    Raises:
    - AuthError if request does not contain HTTP header `Authorization`.
    - AuthError if HTTP header `Authorization` does not contain a bearer
        token.

    Returns:
    - (str) Token from `Authorization` header
        (i.e. content after `Bearer ` prefix).
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description":
                    "Authorization header must start with 'Bearer'."
            },
            401,
        )

    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found."}, 401
        )

    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
            },
            401,
        )

    token = parts[1]
    return token


class AuthorizationToken:
    """A class to get information from a JWT authorization token.

    Wrap a JWT token payload and allows convenient access to
    some of its fields.
    """

    SUBJECT_KEY = "sub"
    PERMISSIONS_KEY = "permissions"
    EXPIRES_AT_KEY = "exp"

    def __init__(self, token_payload):
        self._payload = token_payload

        if AuthorizationToken.SUBJECT_KEY not in token_payload:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Subject not included in JWT.",
                },
                400,
            )

        self._subject = token_payload[AuthorizationToken.SUBJECT_KEY]

        if AuthorizationToken.PERMISSIONS_KEY not in token_payload:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Permissions not included in JWT.",
                },
                400,
            )

        self._permissions = token_payload[AuthorizationToken.PERMISSIONS_KEY]

        if AuthorizationToken.EXPIRES_AT_KEY not in token_payload:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Expires at timestamp missing in JWT.",
                },
                400,
            )

        expiration_timestamp = token_payload[AuthorizationToken.EXPIRES_AT_KEY]
        self._expires_at = datetime.fromtimestamp(expiration_timestamp, tz=UTC)

    def get_subject(self):
        return self._subject

    def get_permissions(self):
        return self._permissions

    def check_permission(self, permission):
        if permission is None:
            return True

        if permission not in self._permissions:
            raise AuthError(
                {
                    "code": "unauthorized",
                    "description": "Permission not found.",
                },
                403,
            )
        return True

    def get_expires_at(self):
        return self._expires_at

    def get_payload(self):
        return self._payload


def verify_decode_jwt(token):
    """Check the validity of a JWT token using the Auth0 service.

    Args:
    - token (str): JWT token.

    Raises:
    - AuthError if JWT token header does not specify the key id used
        for signing.
    - AuthError if JWT token header was signed with an unkown key.
    - AuthError if JWT token cannot be parsed.
    - AuthError if JWT token expired.
    - AuthError if JWT token claims are invalid.
    - AuthError of JWT token is missing required fields, e.g.
      subject, permissions or expiration timestamp.

    Returns:
    - (AuthorizationToken) The payload (aka. claims) of the (valid) JWT token
    """

    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization malformed.",
            },
            401,
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return AuthorizationToken(payload)

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, "
                    + "check the audience and issuer.",
                },
                401,
            )
        except Exception as e:
            print(e)
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


def requires_auth(permission=None):
    """Decorator to check autorization for controller functions.

    Args:
    - permission (str, optional): The permission required to perform the
      decorated controller function. Defaults to "".
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if is_auth_explicitly_deactivated():
                token = None
            else:
                token_string = get_token_auth_header()
                token = verify_decode_jwt(token_string)
                token.check_permission(permission)
            return f(token, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
