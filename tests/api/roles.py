import os
import unittest

from app.models import db, Movie, Actor, Role
from .common import FlaskApiTestCase


class RoleEndpointTestCase(FlaskApiTestCase):
    """This class represents the role endpoint test case"""

    """
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    """
    Endpoint: GET /movies/<movie_id>/roles
    """

    def test_get_roles_for_movie_when_movie_exists(self):
        """Test GET all roles for a movie with valid movie id."""

        # GIVEN
        page = 1
        elements_per_page = 2
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            expected_total_roles = movie.roles.count()

            # WHEN
            response = self.client.get(
                f"/api/v1/movies/{movie.id}/roles?page={page}" +
                f"&per_page={elements_per_page}"
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)
            response_body = response.json
            self.check_paginated_result(
                response_body,
                page=page,
                elements_per_page=elements_per_page,
                expected_name_of_paginated_elements="roles",
                expected_total_elements=expected_total_roles,
            )

            # Check result content
            self.assertTrue(
                any(
                    r["character"]
                    == db.session.merge(self.role_alvy_singer).character
                    for r in response_body["roles"]
                )
            )
            self.assertTrue(
                any(
                    r["character"]
                    == db.session.merge(self.role_annie_hall).character
                    for r in response_body["roles"]
                )
            )

    def test_get_roles_for_movie_when_movie_does_not_exist(self):
        """Test GET all roles for a movie with non-existent movie id."""

        # GIVEN
        movie_id = "NOT_EXISTING_ID"

        # WHEN
        response = self.client.get(f"/api/v1/movies/{movie_id}/roles")

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: GET /movies/<movie_id>/roles/<role_id>
    """

    def test_get_role_when_role_exists(self):
        """Test GET a specific role by id for a movie."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_annie_hall)

            # WHEN
            response = self.client.get(
                f"/api/v1/movies/{movie.id}/roles/{role.id}"
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)
            self.response_represents_entity(response.json, role)

    def test_get_role_when_role_does_not_exist(self):
        """Test GET a specific role with non-existent role id."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role_id = "NOT_EXISTING_ID"

            # WHEN
            response = self.client.get(
                f"/api/v1/movies/{movie.id}/roles/{role_id}"
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    def test_get_role_when_movie_does_not_exist(self):
        """Test GET a specific role for a non-existent movie."""

        # GIVEN
        with self.app.app_context():
            movie_id = "NOT_EXISTING_ID"
            role = db.session.merge(self.role_annie_hall)

            # WHEN
            response = self.client.get(
                f"/api/v1/movies/{movie_id}/roles/{role.id}"
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: DELETE /movies/<movie_id>/roles/<role_id>
    """

    def test_delete_role_when_role_exists(self):
        """Test DELETE a specific role by id for a movie."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_alvy_singer)
            role_id = role.id

            # WHEN
            response = self.client.delete(
                f"/api/v1/movies/{movie.id}/roles/{role_id}"
            )

            # THEN
            self.check_is_ok_no_content(response)

            # Verify role is deleted
            deleted_role = (
                db.session.query(Role).filter(Role.id == role_id).first()
            )
            self.assertIsNone(deleted_role)

    def test_delete_role_when_role_does_not_exist(self):
        """Test DELETE a specific role with non-existent role id."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role_id = "NOT_EXISTING_ID"

            # WHEN
            response = self.client.delete(
                f"/api/v1/movies/{movie.id}/roles/{role_id}"
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    def test_delete_role_when_movie_does_not_exist(self):
        """Test DELETE a specific role for a non-existent movie."""

        # GIVEN
        with self.app.app_context():
            movie_id = "NOT_EXISTING_ID"
            role = db.session.merge(self.role_annie_hall)

            # WHEN
            response = self.client.delete(
                f"/api/v1/movies/{movie_id}/roles/{role.id}"
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: POST /movies/<movie_id>/roles
    """

    def test_create_role_with_actor_when_movie_exists(self):
        """Test POST to create a new role with an actor for existing movie."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_reds)
            actor = db.session.merge(self.actor_keira_knightley)
            new_role_data = {
                "character": "Elizabeth Swann",
                "actor_id": actor.id,
            }

            # WHEN
            response = self.client.post(
                f"/api/v1/movies/{movie.id}/roles", json=new_role_data
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json
            movie = db.session.merge(self.movie_reds)
            actor = db.session.merge(self.actor_keira_knightley)

            self.assertIsNotNone(response_body.get("id"))
            self.assertEqual(
                response_body["character"], new_role_data["character"]
            )
            self.assertEqual(response_body["movie_id"], movie.id)
            self.assertEqual(response_body["actor_id"], actor.id)

            # Verify role is created in DB
            created_role = (
                db.session.query(Role)
                .filter(Role.id == response_body["id"])
                .first()
            )
            self.assertIsNotNone(created_role)
            self.assertEqual(
                created_role.character, new_role_data["character"]
            )
            self.assertEqual(created_role.movie_id, movie.id)
            self.assertEqual(created_role.actor_id, actor.id)

    def test_create_role_without_actor_when_movie_exists(self):
        """Test POST to create a new role without actor for existing movie."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_reds)
            new_role_data = {"character": "Journalist"}

            # WHEN
            response = self.client.post(
                f"/api/v1/movies/{movie.id}/roles", json=new_role_data
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json
            movie = db.session.merge(self.movie_reds)

            self.assertIsNotNone(response_body.get("id"))
            self.assertEqual(
                response_body["character"], new_role_data["character"]
            )
            self.assertEqual(response_body["movie_id"], movie.id)
            self.assertIsNone(response_body["actor_id"])

            # Verify role is created in DB
            created_role = (
                db.session.query(Role)
                .filter(Role.id == response_body["id"])
                .first()
            )
            self.assertIsNotNone(created_role)
            self.assertEqual(
                created_role.character, new_role_data["character"]
            )
            self.assertEqual(created_role.movie_id, movie.id)
            self.assertIsNone(created_role.actor_id)

    def test_create_role_when_movie_does_not_exist(self):
        """Test POST to create a new role for a non-existent movie."""

        # GIVEN
        with self.app.app_context():
            movie_id = "NOT_EXISTING_ID"
            actor = db.session.merge(self.actor_keira_knightley)
            new_role_data = {
                "character": "Ghost Character",
                "actor_id": actor.id,
            }

            # WHEN
            response = self.client.post(
                f"/api/v1/movies/{movie_id}/roles", json=new_role_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    def test_create_role_with_missing_character(self):
        """Test POST to create a new role with missing character data."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_reds)
            actor = db.session.merge(self.actor_keira_knightley)
            new_role_data = {"actor_id": actor.id}

            # WHEN
            response = self.client.post(
                f"/api/v1/movies/{movie.id}/roles", json=new_role_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

    def test_create_role_with_non_existent_actor(self):
        """Test POST to create a new role with a non-existent actor."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_reds)
            non_existent_actor_id = "NOT_EXISTING_ID"

            # WHEN
            new_role_data = {
                "character": "Some Character",
                "actor_id": non_existent_actor_id,
            }

            # WHEN
            response = self.client.post(
                f"/api/v1/movies/{movie.id}/roles", json=new_role_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

    """
    Endpoint: PATCH /movies/<movie_id>/roles/<role_id>
    """

    def test_patch_role_update_character(self):
        """Test PATCH to update only the character of an existing role."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_alvy_singer)
            updated_character = "Alvy Singer (Updated)"
            patch_data = {"character": updated_character}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}/roles/{role.id}", json=patch_data
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json
            self.assertEqual(response_body["id"], role.id)
            self.assertEqual(response_body["character"], updated_character)
            self.assertEqual(response_body["actor_id"], role.actor_id)

            # Verify update in DB
            patched_role = (
                db.session.query(Role).filter(Role.id == role.id).first()
            )
            self.assertEqual(patched_role.character, updated_character)

    def test_patch_role_update_actor(self):
        """Test PATCH to update only the actor of an existing role."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_alvy_singer)
            new_actor = db.session.merge(self.actor_keira_knightley)
            patch_data = {"actor_id": new_actor.id}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}/roles/{role.id}", json=patch_data
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json
            new_actor = db.session.merge(self.actor_keira_knightley)

            self.assertEqual(response_body["id"], role.id)
            self.assertEqual(response_body["character"], role.character)
            self.assertEqual(response_body["actor_id"], new_actor.id)

            # Verify update in DB
            patched_role = (
                db.session.query(Role).filter(Role.id == role.id).first()
            )
            self.assertEqual(patched_role.actor_id, new_actor.id)

    def test_patch_role_remove_actor(self):
        """Test PATCH to remove the actor from an existing role."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_alvy_singer)
            patch_data = {"actor_id": None}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}/roles/{role.id}", json=patch_data
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)
            response_body = response.json
            self.assertEqual(response_body["id"], role.id)
            self.assertEqual(response_body["character"], role.character)
            self.assertIsNone(response_body["actor_id"])

            # Verify update in DB
            patched_role = (
                db.session.query(Role).filter(Role.id == role.id).first()
            )
            self.assertIsNone(patched_role.actor_id)

    def test_patch_role_when_role_does_not_exist(self):
        """Test PATCH for a non-existent role."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role_id = "NOT_EXISTING_ID"
            patch_data = {"character": "Non-existent"}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}/roles/{role_id}", json=patch_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    def test_patch_role_when_movie_does_not_exist(self):
        """Test PATCH for a role belonging to a non-existent movie."""

        # GIVEN
        with self.app.app_context():
            role = db.session.merge(self.role_alvy_singer)
            movie_id = "NOT_EXISTING_ID"
            patch_data = {"character": "Non-existent movie role"}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie_id}/roles/{role.id}", json=patch_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 404)

    def test_patch_role_with_empty_character(self):
        """Test PATCH to update character to an empty string."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_alvy_singer)
            patch_data = {"character": ""}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}/roles/{role.id}", json=patch_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

    def test_patch_role_with_non_existent_actor(self):
        """Test PATCH to update actor to a non-existent actor."""

        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)
            role = db.session.merge(self.role_alvy_singer)
            actor_id = "NOT_EXISTING_ID"
            patch_data = {"actor_id": actor_id}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}/roles/{role.id}", json=patch_data
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

    """
    Endpoint: GET /actors/<actor_id>/roles
    """

    def test_get_roles_for_actor_when_actor_exists(self):
        """Test GET all roles for an actor with valid actor id."""

        # GIVEN
        page = 1
        elements_per_page = 2

        with self.app.app_context():
            actor = db.session.merge(self.actor_diane_keaton)
            expected_total_roles = actor.roles.count()

            # WHEN
            response = self.client.get(
                f"/api/v1/actors/{actor.id}/roles?" +
                f"page={page}&per_page={elements_per_page}"
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json
            self.check_paginated_result(
                response_body,
                page=page,
                elements_per_page=elements_per_page,
                expected_name_of_paginated_elements="roles",
                expected_total_elements=expected_total_roles,
            )

            # Verify specific roles
            self.assertTrue(
                any(
                    r["character"]
                    == db.session.merge(self.role_annie_hall).character
                    for r in response_body["roles"]
                )
            )
            self.assertTrue(
                any(
                    r["character"]
                    == db.session.merge(self.role_louise_bryant).character
                    for r in response_body["roles"]
                )
            )

    def test_get_roles_for_actor_when_actor_does_not_exist(self):
        """Test GET all roles for an actor with non-existent actor id."""
        # GIVEN
        actor_id = "NOT_EXISTING_ID"

        # WHEN
        response = self.client.get(f"/api/v1/actors/{actor_id}/roles")

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
