import unittest
import requests

from app.auth import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_AUDIENCE,
)
from .common import FlaskApiTestCase

"""
Some predefined users for testing.
"""


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._cached_access_token = None

    def __repr__(self):
        password_info = "***" if self.password else "<NO PASSWORD DEFINED>"
        return f"User(username={self.username}, password={password_info})"

    def get_access_token(self, cache: bool = True):
        if self.username is None:
            return None

        if not cache:
            self._cached_access_token = None
            return get_access_token_for_user(self)

        if self._cached_access_token is None:
            self._cached_access_token = get_access_token_for_user(self)
        return self._cached_access_token

    def clear_access_token(self):
        self._cached_access_token = None


UNAUTHENTICATED_USER = User(username=None, password=None)

CASTING_ASSISTANT = User(
    username="casting.assistant@test.com", password="l$ksdf92q3wkmm&qlasdfuq23"
)

CASTING_DIRECTOR = User(
    username="casting.director@test.com", password="?w3qrnwerf7843w2rkl98wef,"
)

EXECUTIVE_PRODUCER = User(
    username="executive.producer@test.com",
    password="9821m3i9k03kle2j430.,23io3as",
)


"""
Helper methods to get valid access tokens for
the test users.
"""


def get_access_token_for_user(user: User):
    """
    Retrieves an access token from Auth0 for a given user.

    This uses the 'Password' grant type, which should only be used
    by trusted first-party applications.
    """
    url = f"https://{AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "password",
        "username": user.username,
        "password": user.password,
        "audience": AUTH0_AUDIENCE,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }

    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")


def get_authorization_header_for_user(user, cache: bool = True):
    access_token = user.get_access_token(cache)
    if access_token is None:
        return {}
    return {"Authorization": f"Bearer {access_token}"}


"""
Authorization Test Case.
"""


class AuthTestCase(FlaskApiTestCase):
    """This class represents the auth test case"""

    # ----------------------------------------------------------------
    # - Control of auth checks for tests
    # ----------------------------------------------------------------

    def auth_checks_required_for_testcase(self):
        return True

    """
    Write at least two test for each role, one success case
    and one failure case.
    """

    """User without authentication"""

    """
    Endpoint: GET /movies, requiring permission get:movie
    when user is not authenticated.
    """

    def test_unauthenticated_user_cannot_get_movies(self):
        """Test that an unauthenticated user cannot get movies."""
        # GIVEN
        user = UNAUTHENTICATED_USER

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        response = self.client.get(
            "/api/v1/movies", headers=request_headers_for_user
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 401)

    """
    Endpoint: POST /actors, requiring permission add:actor
    when user is not authenticated.
    """

    def test_unauthenticated_user_cannot_create_actors(self):
        """Test that an unauthenticated user cannot create actors."""
        # GIVEN
        user = UNAUTHENTICATED_USER

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {"name": "The Dude", "birth_date": "1977-10-10"}

        # WHEN
        response = self.client.post(
            "/api/v1/actors",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 401)

    """
    Endpoint: POST /movies, requiring permission add:movie
    when user is not authenticated.
    """

    def test_unauthenticated_user_cannot_create_movies(self):
        """Test that an unauthenticated user cannot create movies."""
        # GIVEN
        user = UNAUTHENTICATED_USER

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {
            "title": "The Woman that moved to Cabin 13",
            "release_date": "2028-01-12",
        }

        # WHEN
        response = self.client.post(
            "/api/v1/movies",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 401)

    """Role: Casting Assistant"""

    """
    Endpoint: GET /movies, requiring permission get:movie
    which a user with role CASTING_ASSISTENT has.
    """

    def test_casting_assistent_can_get_movies(self):
        """Test that casting assistent can get movies."""
        # GIVEN
        user = CASTING_ASSISTANT

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        response = self.client.get(
            "/api/v1/movies", headers=request_headers_for_user
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

    """
    Endpoint: POST /actors, requiring permission add:actor
    which a user with role CASTING_ASSISTENT does not have.
    """

    def test_casting_assistent_cannot_create_actors(self):
        """Test that casting assistent cannot create actors."""
        # GIVEN
        user = CASTING_ASSISTANT

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {"name": "The Dude", "birth_date": "1977-10-10"}

        # WHEN
        response = self.client.post(
            "/api/v1/actors",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 403)

    """
    Endpoint: POST /movies, requiring permission add:movie
    which a user with role CASTING_ASSISTENT does not have.
    """

    def test_casting_assistent_cannot_create_movies(self):
        """Test that casting assistent cannot create movies."""
        # GIVEN
        user = CASTING_ASSISTANT

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {
            "title": "The Woman that moved to Cabin 13",
            "release_date": "2028-01-12",
        }

        # WHEN
        response = self.client.post(
            "/api/v1/movies",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 403)

    """Role: Casting Director"""

    """
    Endpoint: GET /movies, requiring permission get:movie
    which a user with role CASTING_DIRECTOR has.
    """

    def test_casting_director_can_get_movies(self):
        """Test that casting director can get movies."""
        # GIVEN
        user = CASTING_DIRECTOR

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        response = self.client.get(
            "/api/v1/movies", headers=request_headers_for_user
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

    """
    Endpoint: POST /actors, requiring permission add:actor
    which a user with role CASTING_DIRECTOR has.
    """

    def test_casting_director_can_create_actors(self):
        """Test that casting director can create actors."""
        # GIVEN
        user = CASTING_DIRECTOR

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {"name": "The Dude", "birth_date": "1977-10-10"}

        # WHEN
        response = self.client.post(
            "/api/v1/actors",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

    """
    Endpoint: POST /movies, requiring permission add:movie
    which a user with role CASTING_DIRECTOR does not have.
    """

    def test_casting_director_cannot_create_movies(self):
        """Test that casting director cannot create movies."""
        # GIVEN
        user = CASTING_DIRECTOR

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {
            "title": "The Woman that moved to Cabin 13",
            "release_date": "2028-01-12",
        }

        # WHEN
        response = self.client.post(
            "/api/v1/movies",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 403)

    """Role: Exceutive Producer"""

    """
    Endpoint: GET /movies, requiring permission get:movie
    which a user with role EXECUTIVE_PRODUCER has.
    """

    def test_executive_producer_can_get_movies(self):
        """Test that executive producer can get movies."""
        # GIVEN
        user = EXECUTIVE_PRODUCER

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        response = self.client.get(
            "/api/v1/movies", headers=request_headers_for_user
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

    """
    Endpoint: POST /actors, requiring permission add:actor
    which a user with role EXECUTIVE_PRODUCER has.
    """

    def test_executive_producer_can_create_actors(self):
        """Test that casting director can create actors."""
        # GIVEN
        user = EXECUTIVE_PRODUCER

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {"name": "The Dude", "birth_date": "1977-10-10"}

        # WHEN
        response = self.client.post(
            "/api/v1/actors",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

    """
    Endpoint: POST /movies, requiring permission add:movie
    which a user with role EXECUTIVE_PRODUCER has.
    """

    def test_executive_producer_can_create_movies(self):
        """Test that casting director can create movies."""
        # GIVEN
        user = EXECUTIVE_PRODUCER

        # WHEN
        request_headers_for_user = get_authorization_header_for_user(user)
        request_body = {
            "title": "The Woman that moved to Cabin 13",
            "release_date": "2028-01-12",
        }

        # WHEN
        response = self.client.post(
            "/api/v1/movies",
            json=request_body,
            headers=request_headers_for_user,
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
