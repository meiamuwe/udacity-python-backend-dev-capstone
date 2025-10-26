import unittest

from app.models import db, Movie
from .common import FlaskApiTestCase


class MovieEndpointTestCase(FlaskApiTestCase):
    """This class represents the movie endpoint test case"""

    """
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    """
    Endpoint: GET /movies
    """

    def test_get_movies_page_when_page_exists(self):
        """Test GET all on resource `movies` with valid page."""
        # GIVEN
        page = 1
        elements_per_page = 2

        # WHEN
        response = self.client.get(
            f"/api/v1/movies?page={page}&per_page={elements_per_page}"
        )

        # THEN
        self.check_is_json_and_status_is_ok(response)

        response_body = response.json

        self.check_paginated_result(
            response_body,
            page=page,
            elements_per_page=elements_per_page,
            expected_name_of_paginated_elements="movies",
            expected_total_elements=3,
        )

    def test_get_movies_page_when_page_does_not_exist(self):
        """Test GET all on resource `movies` with page that does not exist."""
        # GIVEN
        page = 3
        elements_per_page = 2

        # WHEN
        response = self.client.get(
            f"/api/v1/movies?page={page}&per_page={elements_per_page}"
        )

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: GET /movies/<movie_id>
    """

    def test_get_movie_when_movie_exists(self):
        """Test GET by id on resource `movies` with valid id."""
        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)

            # WHEN
            response = self.client.get(f"/api/v1/movies/{movie.id}")

            # THEN
            self.check_is_json_and_status_is_ok(response)
            self.response_represents_entity(response.json, movie)

    def test_get_movie_when_movie_does_not_exist(self):
        """Test GET by id on resource `movies` with invalid id."""
        # GIVEN
        movie_id = "NOT_EXISTING_ID"

        # WHEN
        response = self.client.get(f"/api/v1/movies/{movie_id}")

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)

    """
    Endpoint: POST /movies
    """

    def test_create_movie_when_valid_data_provided(self):
        """Test POST on resource `movies` with valid data."""
        # GIVEN
        with self.app.app_context():
            request_body = {
                "title": "The Woman in Cabin 10",
                "release_date": "2025-10-10",
            }

            # WHEN
            response = self.client.post("/api/v1/movies", json=request_body)

            # THEN
            self.check_is_json_and_status_is_ok(response)

            response_body = response.json

            resource_id = response_body.get("id", None)
            self.assertIsNotNone(
                resource_id, "Response must contain a field 'id'"
            )

            self.response_contains_data(response_body, request_body)

            new_movie = Movie.query.filter(Movie.id == resource_id).first()
            self.assertIsNotNone(
                new_movie, "Expected database entity not found"
            )

            self.response_represents_entity(response_body, new_movie)

    def test_create_movie_when_invalid_data_provided(self):
        """Test POST on resource `movies` with invalid data."""
        # GIVEN
        with self.app.app_context():
            request_body = {"title": "The Woman in Cabin 10"}

            number_of_movies_before = Movie.query.count()

            # WHEN
            response = self.client.post("/api/v1/movies", json=request_body)

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

            self.assertEqual(
                number_of_movies_before,
                Movie.query.count(),
                "Number of movies must not change!",
            )

    """
    Endpoint: PUT /movies/<movie_id>
    """

    def test_update_movie_whith_valid_data(self):
        """Test PUT by id on resource `movies` with valid id."""
        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)

            request_body = {
                "title": "Some different title!",
                "release_date": "2025-01-01",
            }

            # WHEN
            response = self.client.put(
                f"/api/v1/movies/{movie.id}", json=request_body
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            updated_movie = Movie.query.filter(Movie.id == movie.id).first()
            self.response_represents_entity(response.json, updated_movie)
            self.response_contains_data(response.json, request_body)

    def test_update_movie_whith_invalid_data(self):
        """Test PUT by id on resource `movies` with valid id."""
        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)

            request_body = {"title": "Some different title!"}

            # WHEN
            response = self.client.put(
                f"/api/v1/movies/{movie.id}", json=request_body
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

            movie_to_update = Movie.query.filter(Movie.id == movie.id).first()
            self.assertEqual(movie_to_update, movie, "Movie must not change!")

    """
    Endpoint: PATCH /movies/<movie_id>
    """

    def test_partial_update_movie_whith_valid_data(self):
        """Test PATCH by id on resource `movies` with valid id."""
        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)

            request_body = {"title": "Some different title!"}

            # WHEN
            response = self.client.patch(
                f"/api/v1/movies/{movie.id}", json=request_body
            )

            # THEN
            self.check_is_json_and_status_is_ok(response)

            updated_movie = Movie.query.filter(Movie.id == movie.id).first()
            self.response_represents_entity(response.json, updated_movie)
            self.response_contains_data(response.json, request_body)

    def test_partial_update_movie_whith_invalid_data(self):
        """Test PATCH by id on resource `movies` with invalid id."""
        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)

            request_body = {"title": ""}

            # WHEN
            response = self.client.put(
                f"/api/v1/movies/{movie.id}", json=request_body
            )

            # THEN
            self.check_is_json_error_response_with_error_code(response, 400)

            movie_to_update = Movie.query.filter(Movie.id == movie.id).first()
            self.assertEqual(movie_to_update, movie, "Movie must not change!")

    """
    Endpoint: DELETE /movies/<movie_id>
    """

    def test_delete_movie_when_existing(self):
        """Test DELETE by id on resource `movies` with valid id."""
        # GIVEN
        with self.app.app_context():
            movie = db.session.merge(self.movie_annie_hall)

            # WHEN
            response = self.client.delete(f"/api/v1/movies/{movie.id}")

            # THEN
            self.check_is_ok_no_content(response)

            deleted_movie = Movie.query.filter(Movie.id == movie.id).first()
            self.assertIsNone(
                deleted_movie,
                "Deleted movie must no longer exist in the database.",
            )

    def test_delete_movie_when_not_existing(self):
        """Test DELETE by id on resource `movies` with invalid id."""
        # GIVEN
        movie_id = "NOT_EXISTING_ID"

        # WHEN
        response = self.client.delete(f"/api/v1/movies/{movie_id}")

        # THEN
        self.check_is_json_error_response_with_error_code(response, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
