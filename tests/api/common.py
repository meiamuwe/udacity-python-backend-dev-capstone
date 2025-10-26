import os
import unittest

from app.api import create_app
from app.helper import to_date
from app.models import db, Movie, Actor, Role
from app.auth import disable_auth_checks_explicitly_for_testing


from abc import ABC


class FlaskApiTestCase(ABC, unittest.TestCase):
    # ----------------------------------------------------------------
    # - Control of auth checks for tests
    # ----------------------------------------------------------------

    def auth_checks_required_for_testcase(self):
        return False

    # ----------------------------------------------------------------
    # - SetUp and TearDown
    # ----------------------------------------------------------------

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = os.environ.get("DATABASE_URL")

        # Create app with the test configuration
        self.app = create_app(
            {
                "SQLALCHEMY_DATABASE_URI": self.database_path,
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "TESTING": True,
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.set_up_database_content(db)

        if self.auth_checks_required_for_testcase():
            disable_auth_checks_explicitly_for_testing(False)
        else:
            disable_auth_checks_explicitly_for_testing(True)

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            self.clean_database_content(db)
            db.session.close()

    def set_up_database_content(self, db):
        self.movie_annie_hall = Movie(
            title="Annie Hall", release_date=to_date("1977-04-20")
        )
        self.movie_reds = Movie(
            title="Reds", release_date=to_date("1981-12-25")
        )
        self.movie_the_shawshank_redemption = Movie(
            title="The Shawshank Redemption",
            release_date=to_date("1994-10-14"),
        )

        db.session.add(self.movie_annie_hall)
        db.session.add(self.movie_reds)
        db.session.add(self.movie_the_shawshank_redemption)

        self.actor_keira_knightley = Actor(
            name="Keira Knightley", birth_date=to_date("1985-03-26")
        )
        self.actor_diane_keaton = Actor(
            name="Diane Keaton", birth_date=to_date("1946-01-05")
        )
        self.actor_woody_allen = Actor(
            name="Woody Allen", birth_date=to_date("1935-11-30")
        )

        db.session.add(self.actor_keira_knightley)
        db.session.add(self.actor_diane_keaton)
        db.session.add(self.actor_woody_allen)

        self.role_alvy_singer = Role(
            character="Alvy Singer",
            movie=self.movie_annie_hall,
            actor=self.actor_woody_allen,
        )
        self.role_annie_hall = Role(
            character="Annie Hall",
            movie=self.movie_annie_hall,
            actor=self.actor_diane_keaton,
        )
        self.role_louise_bryant = Role(
            character="Louise Bryant",
            movie=self.movie_reds,
            actor=self.actor_diane_keaton,
        )
        self.role_john_reed = Role(
            character="John Reed", movie=self.movie_reds
        )
        self.role_ellie_boyd_redding = Role(
            character="Ellis Boyd 'Red' Redding",
            movie=self.movie_the_shawshank_redemption,
        )

        db.session.add(self.role_alvy_singer)
        db.session.add(self.role_annie_hall)
        db.session.add(self.role_louise_bryant)
        db.session.add(self.role_john_reed)
        db.session.add(self.role_ellie_boyd_redding)

        db.session.commit()

    def clean_database_content(self, db):
        Movie.query.delete()
        Actor.query.delete()
        Role.query.delete()

        db.session.commit()

    # ----------------------------------------------------------------
    # - HELPER
    # ----------------------------------------------------------------

    def check_is_json_error_response_with_error_code(
        self, response, error_code
    ):
        """Checks response is an error with common JSON structure."""

        self.assertEqual(
            response.status_code,
            error_code,
            f"Response status code must be '{error_code}'.",
        )
        self.assertEqual(
            response.headers["Content-Type"],
            "application/json",
            "Response must have content type 'application/json'.",
        )

        response_body = response.json
        success = response_body.get("success", None)
        error_code = response_body.get("error_code", None)
        message = response_body.get("message", None)

        # Test required fields
        self.assertNotEqual(
            success, None, "Response must contain a field 'success'"
        )
        self.assertTrue(
            error_code, "Response must contain a field 'error_code'"
        )
        self.assertTrue(message, "Response must contain a field 'message'")

        # Test success details
        self.assertEqual(
            success, False, "Response must report success as false."
        )

        # Test error_code details
        self.assertEqual(
            error_code,
            f"{error_code}",
            f"Response must report error_code as '{error_code}'.",
        )

        # Test message details
        self.assertNotEqual(
            message, "", "Response must contain a non-empty message."
        )

    def check_is_json_and_status_is_ok(self, response, status_code=200):
        """Checks if the status code is success code and content is JSON."""

        self.assertEqual(
            response.status_code,
            status_code,
            "Response status code is not correct!",
        )
        self.assertEqual(
            response.headers["Content-Type"],
            "application/json",
            "Response must have content type 'application/json'.",
        )

    def check_is_ok_no_content(self, response):
        """Checks if the status code is 204 and content is empty."""

        self.assertEqual(
            response.status_code, 204, "Response status code is not correct!"
        )
        self.assertEqual(response.data, b"", "Response body must be empty!")

    def check_paginated_result(
        self,
        response_body,
        page,
        elements_per_page,
        expected_name_of_paginated_elements,
        expected_total_elements,
    ):
        elements = response_body.get(expected_name_of_paginated_elements, None)
        name_of_total_elements = f"total_{expected_name_of_paginated_elements}"
        total_elements = response_body.get(name_of_total_elements, None)
        current_page = response_body.get("current_page", None)
        total_pages = response_body.get("total_pages", None)

        # Test required fields
        self.assertTrue(
            elements,
            "Response must contain a field '{name_of_paginated_elements}'",
        )
        self.assertTrue(
            total_elements,
            "Response must contain a field '{name_of_total_elements}'",
        )
        self.assertTrue(
            current_page, "Response must contain a field 'current_page'"
        )
        self.assertTrue(
            total_pages,
            "Response must contain a field 'total_pages'",
        )

        # Test elements details
        elements_on_previous_pages = (page - 1) * elements_per_page

        expected_elements_on_current_page = (
            elements_per_page
            if (total_elements - elements_on_previous_pages)
            >= elements_per_page
            else (total_elements - elements_on_previous_pages)
        )

        self.assertEqual(
            len(elements),
            expected_elements_on_current_page,
            f"Response for page {page} must contain " +
            f"{expected_elements_on_current_page} questions.",
        )
        # Test total_elements details
        self.assertEqual(
            total_elements,
            expected_total_elements,
            f"Response must specifiy {expected_total_elements} " +
            f"'{name_of_total_elements}'.",
        )
        # Test current_page details
        self.assertEqual(
            current_page,
            page,
            f"Response must specifiy current_page is {page}.",
        )
        # Test total_pages details
        expected_total_pages = (
            expected_total_elements // elements_per_page
        ) + (1 if expected_total_elements % elements_per_page > 0 else 0)

        self.assertEqual(
            total_pages,
            expected_total_pages,
            f"Response must specifiy {expected_total_pages} total_pages.",
        )

    def response_represents_entity(self, response_body, entity):
        self.assertEqual(response_body, entity.format())

    def response_contains_data(self, response_body, expected_data):
        for key, value in expected_data.items():
            self.assertEqual(response_body.get(key, None), value)
