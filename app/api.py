from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect,
    render_template,
    url_for,
)
from flask_cors import CORS
from flask_migrate import Migrate
from urllib.parse import urlencode

from app.models import setup_db, Movie, Actor, Role
from app.helper import to_date

from app.auth import (
    AUTH0_AUDIENCE,
    AUTH0_CLIENT_ID,
    AUTH0_DOMAIN,
    AUTH0_CALLBACK_SCHEME,
    AUTH0_CALLBACK_SERVER,
)
from app.auth import AuthError, requires_auth


"""
The URL base paths.
"""
API_BASE_PATH = "/api/v1"
WEB_BASE_PATH = ""

"""
Constants for pagination.
"""
MOVIES_PER_PAGE = 10
ACTORS_PER_PAGE = 10
ROLES_PER_PAGE = 10


NO_CONTENT = ""


"""
Factory function to create and configure the application.
"""


def create_app(test_config=None):
    """Create and configure the application."""

    app = Flask(__name__)

    """
    Setup the database
    """
    if test_config is None:
        db = setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        db = setup_db(app, database_path=database_path)

    """
    Enable DB migrations
    """
    Migrate(app, db)

    """
    Set up CORS for the API. Allow '*' for origins.
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow for CORS.
    """

    @app.after_request
    def add_cors_response_headers(response):
        """Set CORS headers for each response from the application."""
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
        )
        return response

    """
    The API definition.
    """

    """
    Health check
    """
    @app.route("/health", methods=["GET"])
    def health_check():
        return "Service is up!", 200
        
    """
    Index
    """
    @app.route("/", methods=["GET"])
    def index():
        return redirect(url_for("user_login"))
    
    
    """
    User Login
    using an external Auth Provider (Auth0)
    """

    @app.route("/login", methods=["GET"])
    def user_login():
        """Triggers external authentication with Auth0 and callback."""
        user_home_internal_url = url_for("user_home")
        user_home_external_url = "{}://{}{}".format(
            AUTH0_CALLBACK_SCHEME,
            AUTH0_CALLBACK_SERVER,
            user_home_internal_url,
        )
        query_parameters = urlencode(
            {
                "audience": AUTH0_AUDIENCE,
                "response_type": "token",
                "client_id": AUTH0_CLIENT_ID,
                "redirect_uri": user_home_external_url,
            }
        )
        auth0_login_with_redirect_url = (
            f"https://{AUTH0_DOMAIN}/authorize?{query_parameters}"
        )
        return redirect(location=auth0_login_with_redirect_url)

    @app.route(f"{WEB_BASE_PATH}/user-home", methods=["GET"])
    def user_home():
        """Show user home page."""

        user_logout_internal_url = url_for("user_logout")
        user_logout_external_url = "{}://{}{}".format(
            AUTH0_CALLBACK_SCHEME,
            AUTH0_CALLBACK_SERVER,
            user_logout_internal_url,
        )
        
        query_parameters = urlencode(
            {
                "client_id": AUTH0_CLIENT_ID,
                "returnTo": user_logout_external_url,
            }
        )
        
        auth0_logout_with_redirect_url = (
            f"https://{AUTH0_DOMAIN}/v2/logout?{query_parameters}"
        )
        
        print("auth0_logout_with_redirect_url = ", auth0_logout_with_redirect_url)

        return render_template(
            "user-home.html", logout_url=auth0_logout_with_redirect_url
        )

    @app.route(f"{WEB_BASE_PATH}/logout", methods=["GET"])
    def user_logout():
        """Renders the logout confirmation page."""
        return render_template("logout.html")

    """
    Resource: movies
    """

    @app.route(f"{API_BASE_PATH}/movies", methods=["GET"])
    @requires_auth(permission="get:movie")
    def get_movies(auth_token):
        """List all movies."""

        # Support pagination:
        # Get movies for page with "page" query parameter as default,
        # or 1 if missing.
        movies_query = db.select(Movie).order_by(Movie.title.asc())

        movies = db.paginate(
            movies_query,
            per_page=None,
            max_per_page=MOVIES_PER_PAGE,
            error_out=True,
            count=True,
        )

        formatted_movies = [movie.format() for movie in movies.items]

        return jsonify(
            {
                "movies": formatted_movies,
                "total_movies": movies.total,
                "current_page": movies.page,
                "total_pages": movies.pages,
            }
        )

    @app.route("{}/movies/<movie_id>".format(API_BASE_PATH), methods=["GET"])
    @requires_auth(permission="get:movie")
    def get_movie(auth_token, movie_id):
        """Get a movie by id."""

        movie = Movie.query.filter(Movie.id == movie_id).first_or_404()

        return jsonify(movie.format())

    @app.route(
        "{}/movies/<movie_id>".format(API_BASE_PATH), methods=["DELETE"]
    )
    @requires_auth(permission="delete:movie")
    def delete_movie(auth_token, movie_id):
        """Delete a movie by id."""

        movie = Movie.query.filter(Movie.id == movie_id).first_or_404()

        try:
            db.session.delete(movie)
            db.session.commit()

            return NO_CONTENT, 204

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route(f"{API_BASE_PATH}/movies", methods=["POST"])
    @requires_auth(permission="add:movie")
    def create_movie(auth_token):
        """Create a new movie."""

        # Validate input data

        title = request.json.get("title", None)
        release_date = to_date(request.json.get("release_date", None))

        assert title, "No title provided!"
        assert release_date, "No valid release date provided!"

        # Create new movie in database
        try:
            new_movie = Movie(title=title, release_date=release_date)

            db.session.add(new_movie)
            db.session.commit()

            return jsonify(new_movie.format())

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route("{}/movies/<movie_id>".format(API_BASE_PATH), methods=["PUT"])
    @requires_auth(permission="modify:movie")
    def update_movie(auth_token, movie_id):
        """Update a movie by id."""

        # Validate input data

        title = request.json.get("title", None)
        release_date = to_date(request.json.get("release_date", None))

        assert title, "No title provided!"
        assert release_date, "No valid release date provided!"

        # Get existing movie
        movie = Movie.query.filter(Movie.id == movie_id).first_or_404()

        # Update existing movie in database
        try:
            movie.title = title
            movie.release_date = release_date
            db.session.commit()

            return jsonify(movie.format())

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route("{}/movies/<movie_id>".format(API_BASE_PATH), methods=["PATCH"])
    @requires_auth(permission="modify:movie")
    def patch_movie(auth_token, movie_id):
        """Partially update a movie by id."""

        movie = Movie.query.filter(Movie.id == movie_id).first_or_404()

        # Validate given input data and
        # updated existing movie
        try:
            title = request.json.get("title", None)
            if title is not None:
                assert title, "No title provided!"
                movie.title = title

            release_date = request.json.get("release_date", None)
            if release_date:
                new_release_date = to_date(release_date)
                assert new_release_date, "No valid release date provided!"
                movie.release_date = new_release_date

            db.session.commit()

            return jsonify(movie.format())

        except AssertionError as err:
            db.session.rollback()
            raise err

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    """
    Resource: actors
    """

    @app.route(f"{API_BASE_PATH}/actors", methods=["GET"])
    @requires_auth(permission="get:actor")
    def get_actors(auth_token):
        """List all actors."""

        # Support pagination:
        # Get movies for page with "page" query parameter as default,
        # or 1 if missing.
        actors_query = db.select(Actor).order_by(Actor.name.asc())

        actors = db.paginate(
            actors_query,
            per_page=None,
            max_per_page=ACTORS_PER_PAGE,
            error_out=True,
            count=True,
        )

        formatted_actors = [actor.format() for actor in actors]

        return jsonify(
            {
                "actors": formatted_actors,
                "total_actors": actors.total,
                "current_page": actors.page,
                "total_pages": actors.pages,
            }
        )

    @app.route("{}/actors/<actor_id>".format(API_BASE_PATH), methods=["GET"])
    @requires_auth(permission="get:actor")
    def get_actor(auth_token, actor_id):
        """Get an actor by id."""

        actor = Actor.query.filter(Actor.id == actor_id).first_or_404()

        return jsonify(actor.format())

    @app.route(
        "{}/actors/<actor_id>".format(API_BASE_PATH), methods=["DELETE"]
    )
    @requires_auth(permission="delete:actor")
    def delete_actor(auth_token, actor_id):
        """Delete an actor by id."""

        actor = Actor.query.filter(Actor.id == actor_id).first_or_404()

        try:
            db.session.delete(actor)
            db.session.commit()

            return NO_CONTENT, 204

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route(f"{API_BASE_PATH}/actors", methods=["POST"])
    @requires_auth(permission="add:actor")
    def create_actor(auth_token):
        """Create a new actor."""

        # Validate input data
        name = request.json.get("name", None)
        birth_date = to_date(request.json.get("birth_date", None))

        assert name, "No name provided!"
        assert birth_date, "No birth date provided!"

        # Create new actor in database
        try:
            new_actor = Actor(name=name, birth_date=birth_date)

            db.session.add(new_actor)
            db.session.commit()

            return jsonify(new_actor.format())

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route("{}/actors/<actor_id>".format(API_BASE_PATH), methods=["PUT"])
    @requires_auth(permission="modify:actor")
    def update_actor(auth_token, actor_id):
        """Update an actor by id."""

        # Validate input data

        name = request.json.get("name", None)
        birth_date = to_date(request.json.get("birth_date", None))

        assert name, "No name provided!"
        assert birth_date, "No valid birth date provided!"

        # Get existing actor
        actor = Actor.query.filter(Actor.id == actor_id).first_or_404()

        # Update existing actor in database
        try:
            actor.name = name
            actor.birth_date = birth_date
            db.session.commit()

            return jsonify(actor.format())

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route("{}/actors/<actor_id>".format(API_BASE_PATH), methods=["PATCH"])
    @requires_auth(permission="modify:actor")
    def patch_actor(auth_token, actor_id):
        """Partially update an actor by id."""

        actor = Actor.query.filter(Actor.id == actor_id).first_or_404()

        # Validate given input data and
        # updated existing actor
        try:
            name = request.json.get("name", None)
            if name is not None:
                assert name, "No name provided!"
                actor.name = name

            birth_date = request.json.get("birth_date", None)
            if birth_date:
                new_birth_date = to_date(birth_date)
                assert new_birth_date, "No valid birth date provided!"
                actor.birth_date = new_birth_date

            db.session.commit()

            return jsonify(actor.format())

        except AssertionError as err:
            db.session.rollback()
            raise err

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    """
    Sub-resource: roles
    """

    @app.route(f"{API_BASE_PATH}/movies/<movie_id>/roles", methods=["GET"])
    @requires_auth(permission="get:movie")
    def get_roles_for_movie(auth_token, movie_id):
        """Get all roles for a movie by id."""

        # Check that movie exists
        Movie.query.filter(Movie.id == movie_id).first_or_404()

        # Support pagination:
        # Get movies for page with "page" query parameter as default,
        # or 1 if missing.
        roles_query = (
            db.select(Role)
            .where(Role.movie_id == movie_id)
            .order_by(Role.character.asc())
        )

        # roles_query = movie.roles.order_by(Role.character.asc())

        roles = db.paginate(
            roles_query,
            per_page=None,
            max_per_page=ROLES_PER_PAGE,
            error_out=True,
            count=True,
        )

        formatted_roles = [role.format() for role in roles]

        return jsonify(
            {
                "roles": formatted_roles,
                "total_roles": roles.total,
                "current_page": roles.page,
                "total_pages": roles.pages,
            }
        )

    @app.route(
        f"{API_BASE_PATH}/movies/<movie_id>/roles/<role_id>", methods=["GET"]
    )
    @requires_auth(permission="get:movie")
    def get_role(auth_token, movie_id, role_id):
        """Get role by id."""

        role = Role.query.filter(
            Role.movie_id == movie_id, Role.id == role_id
        ).first_or_404()

        return jsonify(role.format())

    @app.route(
        f"{API_BASE_PATH}/movies/<movie_id>/roles/<role_id>",
        methods=["DELETE"],
    )
    @requires_auth(permission="modify:movie")
    def delete_role(auth_token, movie_id, role_id):
        """Delete a role by id."""

        role = Role.query.filter(
            Role.movie_id == movie_id, Role.id == role_id
        ).first_or_404()

        try:
            db.session.delete(role)
            db.session.commit()

            return NO_CONTENT, 204

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route(f"{API_BASE_PATH}/movies/<movie_id>/roles", methods=["POST"])
    @requires_auth(permission="modify:movie")
    def create_role(auth_token, movie_id):
        """Create a new role for a movie."""

        # Validate input data

        character = request.json.get("character", None)
        actor_id = request.json.get("actor_id", None)

        assert character, "No character provided!"

        movie = Movie.query.filter(Movie.id == movie_id).first()

        if movie is None:
            abort(404)

        actor = None
        if actor_id is not None:
            actor = Actor.query.filter(Actor.id == actor_id).first()

            assert actor, "Actor not found!"

        # Create new role in database
        try:
            new_role = Role(character=character, movie=movie, actor=actor)

            db.session.add(new_role)
            db.session.commit()

            return jsonify(new_role.format())

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route(
        f"{API_BASE_PATH}/movies/<movie_id>/roles/<role_id>", methods=["PATCH"]
    )
    @requires_auth(permission="modify:movie")
    def patch_role(auth_token, movie_id, role_id):
        """Partially update a role by id."""

        role = Role.query.filter(
            Role.id == role_id, Role.movie_id == movie_id
        ).first_or_404()

        # Validate given input data and
        # updated existing role

        try:
            character = request.json.get("character", None)
            if character is not None:
                assert character, "No character provided!"
                role.character = character

            actor_id_specified = "actor_id" in request.json
            if actor_id_specified:
                actor_id = request.json.get("actor_id")
                if actor_id is not None:
                    actor = Actor.query.filter(Actor.id == actor_id).first()
                    assert actor, "Actor not found!"
                else:
                    actor = None

                role.actor = actor

            db.session.commit()

            return jsonify(role.format())

        except AssertionError as err:
            db.session.rollback()
            raise err

        except Exception:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    @app.route(f"{API_BASE_PATH}/actors/<actor_id>/roles", methods=["GET"])
    @requires_auth(permission="get:actor")
    def get_roles_for_actor(auth_token, actor_id):
        """Get all roles for an actor by id."""

        # Check that movie exists
        Actor.query.filter(Actor.id == actor_id).first_or_404()

        # Support pagination:
        # Get movies for page with "page" query parameter as default,
        # or 1 if missing.
        roles_query = (
            db.select(Role)
            .where(Role.actor_id == actor_id)
            .order_by(Role.character.asc())
        )

        roles = db.paginate(
            roles_query,
            per_page=ROLES_PER_PAGE,
            error_out=True,
            count=True,
        )

        formatted_roles = [role.format() for role in roles]

        return jsonify(
            {
                "roles": formatted_roles,
                "total_roles": roles.total,
                "current_page": roles.page,
                "total_pages": roles.pages,
            }
        )

    """
    Error handlers
    """

    @app.errorhandler(404)
    def not_found(error):
        """Error handler to generate JSON payload for 404 errors."""
        return jsonify(
            {
                "success": False,
                "error_code": "404",
                "message": "No results found!",
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """Error handler to handle unprocessable errors."""
        return jsonify(
            {
                "success": False,
                "error_code": "422",
                "message": "Request cannot be processed: Invalid input data!",
            }
        ), 422

    @app.errorhandler(400)
    def bad_request(error):
        """Error handler for bad requests."""
        return invalid_input(error)

    @app.errorhandler(AssertionError)
    def assertion_error(error):
        """Error handler for assertion errors."""
        return invalid_input(error)

    def invalid_input(error):
        """Generates JSON payload for 400 errors."""
        message = f"Request cannot be processed: Bad request! {error}"
        return jsonify(
            {
                "success": False,
                "error_code": "400",
                "message": message,
            }
        ), 400

    # Authentication and authorization
    # related problems causing HTTP responses
    # with status 400, 401, 403

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        """Create JSON response for AuthError exceptions."""

        return jsonify(
            {
                "success": False,
                "error_code": str(error.status_code),
                "message": error.error["description"],
            }
        ), error.status_code

    return app
