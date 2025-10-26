import unittest

from app.models import db, Actor
from .common import FlaskApiTestCase


class ActorEndpointTestCase(FlaskApiTestCase):
    """This class represents the actor endpoint test case"""

    """
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    """
    Endpoint: GET /actors
    """

    def test_get_actors_page_when_page_exists(self):
        """Test GET all on resource `actors` with valid page."""
        # GIVEN
        page = 1
        elements_per_page = 2

        # WHEN
        response = self.client.get(
            f"/api/v1/actors?page={page}&per_page={elements_per_page}"
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

        response_body = response.json

        self.check_paginated_result(
            response_body,
            page=page,
            elements_per_page=elements_per_page,
            expected_name_of_paginated_elements="actors",
            expected_total_elements=3,
        )

    def test_get_actors_page_when_page_does_not_exist(self):
        """Test GET all on resource `actors` with page that does not exist."""
        # GIVEN
        page = 3
        elements_per_page = 2

        # WHEN
        response = self.client.get(
            f"/api/v1/actors?page={page}&per_page={elements_per_page}"
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: GET /actors/<movie_id>
    """

    def test_get_actor_when_actor_exists(self):
        """Test GET by id on resource `actors` with valid id."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_diane_keaton)

            # WHEN
            response = self.client.get(f"/api/v1/actors/{actor.id}")

            # THEN
            self.check_is_json_and_status_is_ok(response)
            self.response_represents_entity(response.json, actor)

    def test_get_actor_when_actor_does_not_exist(self):
        """Test GET by id on resource `actors` with invalid id."""
        # GIVEN
        actor_id = "NOT_EXISTING_ID"

        # WHEN
        response = self.client.get(f"/api/v1/actors/{actor_id}")

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: POST /actors
    """

    def test_create_actor_when_valid_data_provided(self):
        """Test POST on resource `actors` with valid data."""
        # GIVEN
        with self.app.app_context():
            request_body = {
                "name": "Morgan Freeman",
                "birth_date": "1937-06-01",
            }

            # WHEN
            response = self.client.post("/api/v1/actors", json=request_body)

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json

            resource_id = response_body.get("id", None)
            self.assertIsNotNone(
                resource_id, "Response must contain a field 'id'"
            )

            self.response_contains_data(response_body, request_body)

            new_actor = Actor.query.filter(Actor.id == resource_id).first()
            self.assertIsNotNone(
                new_actor, "Expected database entity not found"
            )

            self.response_represents_entity(response_body, new_actor)

    def test_create_movie_when_invalid_data_provided(self):
        """Test POST on resource `actors` with invalid data."""
        # GIVEN
        with self.app.app_context():
            request_body = {"name": "Hey Dude"}

            number_of_actors_before = Actor.query.count()

            # WHEN
            response = self.client.post("/api/v1/actors", json=request_body)

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

            self.assertEqual(
                number_of_actors_before,
                Actor.query.count(),
                "Number of actors must not change!",
            )

    """
    Endpoint: PUT /actors/<actor_id>
    """

    def test_update_actor_whith_valid_data(self):
        """Test PUT by id on resource `actors` with valid id."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_diane_keaton)

            request_body = {
                "name": "Diane Keaton (updated)",
                "birth_date": "2025-01-01",
            }

            # WHEN
            response = self.client.put(
                f"/api/v1/actors/{actor.id}", json=request_body
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            updated_actor = Actor.query.filter(Actor.id == actor.id).first()
            self.response_represents_entity(response.json, updated_actor)
            self.response_contains_data(response.json, request_body)

    def test_update_actor_whith_invalid_data(self):
        """Test PUT by id on resource `actors` with valid id."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_diane_keaton)

            request_body = {"name": "Diane Keaton (updated)"}

            # WHEN
            response = self.client.put(
                f"/api/v1/actros/{actor.id}", json=request_body
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

            actor_to_update = Actor.query.filter(Actor.id == actor.id).first()
            self.assertEqual(actor_to_update, actor, "Actor must not change!")

    """
    Endpoint: PATCH /actors/<actor_id>
    """

    def test_partial_update_actor_whith_valid_data(self):
        """Test PATCH by id on resource `actors` with valid id."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_diane_keaton)

            request_body = {"name": "Diane Keaton (updated)"}

            # WHEN
            response = self.client.patch(
                f"/api/v1/actors/{actor.id}", json=request_body
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            updated_actor = Actor.query.filter(Actor.id == actor.id).first()
            self.response_represents_entity(response.json, updated_actor)
            self.response_contains_data(response.json, request_body)

    def test_partial_update_actor_whith_invalid_data(self):
        """Test PATCH by id on resource `actors` with invalid id."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_diane_keaton)

            request_body = {"name": ""}

            # WHEN
            response = self.client.put(
                f"/api/v1/actors/{actor.id}", json=request_body
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

            actor_to_update = Actor.query.filter(Actor.id == actor.id).first()
            self.assertEqual(actor_to_update, actor, "Actor must not change!")

    """
    Endpoint: DELETE  /actors/<actor_id>
    """

    def test_delete_actor_when_existing(self):
        """Test DELETE by id on resource `actors` with valid id."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_keira_knightley)

            # WHEN
            response = self.client.delete(f"/api/v1/actors/{actor.id}")

            # THEN
            self.check_is_ok_no_content(response)

            deleted_actor = Actor.query.filter(Actor.id == actor.id).first()
            self.assertIsNone(
                deleted_actor,
                "Deleted actor must no longer exist in the database.",
            )

    def test_delete_actor_when_existing_but_with_roles(self):
        """Test DELETE by id on resource `actors` with valid id and roles."""
        # GIVEN
        with self.app.app_context():
            actor = db.session.merge(self.actor_woody_allen)

            # WHEN
            response = self.client.delete(f"/api/v1/actors/{actor.id}")

            # THEN
            self.check_is_json_error_response_with_error_code(response, 422)

            actor = db.session.merge(self.actor_woody_allen)
            actor_to_delete = Actor.query.filter(Actor.id == actor.id).first()
            self.assertEqual(actor_to_delete, actor, "Actor must not change.")

    def test_delete_actor_when_not_existing(self):
        """Test DELETE by id on resource `actors` with invalid id."""
        # GIVEN
        movie_id = "NOT_EXISTING_ID"

        # WHEN
        response = self.client.delete(f"/api/v1/actors/{movie_id}")

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
