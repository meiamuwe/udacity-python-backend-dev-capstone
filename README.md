# Python Backend Developer Capstone Project: MovieWorld

This is an implementation of the [capstone project](https://learn.udacity.com/nd0044) of the [Python Backend Developer Nano Degree](https://udacity.com/enrollment/nd0044) program.



# Motivation 

MovieWorld is a casting agency that is responsible for creating movies and managing and assigning actors to those movies. The Executive Producer of the company asked 
to create a web-based API to simplify and streamline the companies' process.

We designed and implemented the desired web-based API in this project. 

## Data model

Our application manages information about movies, the actors who star in them, and the specific roles within those movies. 
The data is organized into three main categories:

*   **Movies**: Represents a film project. Each movie has details like its title and release date.
*   **Actors**: Represents a performer. We keep track of information for each actor, such as their name and birthdate.
*   **Roles**: Represents a specific character or part in a movie. A role links a movie to an actor, but a role might exist without an actor assigned yet, especially during the casting process.

To manage the casting process, we link actors to the movies they are cast in using roles. This allows us to see the cast for any given movie and the filmography for any given actor.

There cannot be more than one role for the same character in a movie.

Roles always are tied to a specific movie. Deleting a movie also deletes all of its roles.
A role however does not depend on an actor, i.e. they can exist independently from actors.
A role in a movie that has not yet been filled, does not have an actor assigned. 

However, if a role is assigned to an actor, then that deleting that actor is not allowed. 
To delete the actor, first the actor has to be unassigned from the role, then it can be deleted.


## Operations on this data model 

The API supports the following operations on the data model: 

### Movies
*   **View Movies**: You can get a list of all movies or view the details of a single movie.
*   **Create Movies**: You can add a new movie to the database.
*   **Update Movies**: You can change the title or release date of an existing movie.
*   **Delete Movies**: You can remove a movie from the database.
*   **View Roles for a Movie**: You can see all the roles associated with a particular movie.
*   **View a Specific Role**: You can view the details of a single role within a movie.
*   **Create Roles**: You can add a new role to a movie, optionally assigning an actor to it.
*   **Update Roles**: You can change the character name for a role or assign/unassign an actor to it.
*   **Delete Roles**: You can remove a specific role from a movie.


### Actors
*   **View Actors**: You can get a list of all actors or view the details of a single actor.
*   **Create Actors**: You can add a new actor to the database.
*   **Update Actors**: You can change the name or birthdate of an existing actor.
*   **Delete Actors**: You can remove an actor from the database.
*   **View Roles for an Actor**: You can see all the roles an actor has been assigned so 

## List of Permissions

We use the following permissions in this project:

| Permission | Description |
|---|---|
| `get:actor` | Get actor over the API |
| `get:movie` | Get movies over the API |
| `add:actor` | Add actor over the API |
| `delete:actor` | Delete actor over the API |
| `modify:actor` | Modify actor over the API |
| `modify:movie` | Modify movie over the API |
| `add:movie` | Add movie over the API |
| `delete:movie` | Delete movies over the API |

## Roles
We have the following predefined roles in this project:


|Role|Permissions|
|----|--------|
|Casting Assistant|`get:actor`, `get:movie`|
|Casting Director|`get:actor`, `get:movie`, `add:actor`, `delete:actor`, `modify:actor`, `modify:movie` |
|Executive Producer|`get:actor`, `get:movie`, `add:actor`, `delete:actor`, `modify:actor`, `modify:movie`, `add:movie`, `delete:movie`|

## Users 

For each role we defined a user for testing:

|Role|Username|Password|
|----|--------|--------|
|Casting Assistant|`casting.assistant@test.com`|`l$ksdf92q3wkmm&qlasdfuq23`|
|Casting Director|`casting.director@test.com`|`?w3qrnwerf7843w2rkl98wef,`|
|Executive Producer|`executive.producer@test.com`|`9821m3i9k03kle2j430.,23io3as`|


# Link to hosted API

The application is deployed on Render.com and can be reached using the following [host](https://movieworld-udacity-capstone.onrender.com). 

Please note, for authentication and authorization, the app uses the *external service provider* [Auth0](https://auth0.com).


# Demo of Deployed API

## User authentication 

The application offers an interactive login demo to demonstrate the authentication and authorization 
with the external service provider Auth0. Please use the following [Login link](https://movieworld-udacity-capstone.onrender.com/login) of the of the applicaton.


## API Tests with Postman

The project includes a Postman testsuite to test the API. The MovieWorld API Test Suite definition can be found [here](MovieWorld-API-Tests.postman_collection.json). 


To execute the tests, you need the tool Postman installed.

The test suite is by default set up for local test and requires the definition of the following variables
before executing the tests (or to use the suite to test the production deployment): 

| Variable | Purpose | Values  |
|----------|---------|---------|
| `baseUrl` | URL for the server, that runs the API | Default value `http://localhost:5000` is suitable for local development. To test the production deployment, please use `https://movieworld-udacity-capstone.onrender.com` instead. |
| `auth0_client_id` | Auth0 client ID | You can find the required value in the project submission comments.|
| `auth0_client_secret` | Auth0 client secret | You can find the required value in the project submission comments.|

The test suite covers the required functionallity of the API extensively, including tests for authorization 
and authentication.


# Project dependencies

The project has been developed with Python 3.13.


It uses the following main python libraries: 

| Dependency         | Version   | Description                                                     |
|--------------------|-----------|-----------------------------------------------------------------|
| Flask              | 3.1.2     | A micro web framework for building web applications in Python.    |
| Flask-SQLAlchemy   | 3.1.1     | Adds SQLAlchemy ORM support to your Flask application.          |
| Flask-Migrate      | 4.1.0     | Handles SQLAlchemy database migrations for Flask apps via Alembic.|
| flask-cors         | 6.0.1     | A Flask extension for handling Cross-Origin Resource Sharing.   |
| SQLAlchemy         | 2.0.44    | The Python SQL toolkit and Object Relational Mapper.            |
| psycopg2-binary    | 2.9.11    | A PostgreSQL database adapter for the Python programming language.|
| Alembic            | 1.17.0    | A lightweight database migration tool for usage with SQLAlchemy.|
| gunicorn           | 23.0.0    | A Python WSGI HTTP Server for UNIX.                             |
| python-jose        | 3.5.0     | A library for JWT, JWS, JWE, JWK, and JWA in Python.            |


All required depencies are listed in [this file](requirements.txt).


# Local development and hosting instructions

## Setting up the local database

We require a PostgresDB installation.

Execute the following commands to set up the database user and database for local 
development and tests: 

```bash
source setup_database_local.sh
psql --username movieworld_test movieworld_test

Enter password: movieworld_test
```

If you want some example data, you can use

```bash
psql --username=movieworld_test -a -f movieworld_db_content.sql

Enter password: movieworld_test
```

## Local development

After check out the project, set up the required environment variables: 

```bash
# Additionally, set up the external Auth Provider configuration
export AUTH0_CLIENT_ID="<See submission comments for the required value>"
export AUTH0_CLIENT_SECRET="<See submission comments for the required value>"

```

Then, you can build and run the application locally: 

```bash
source run_local.sh
```

This automatically, sets up all other environment variables, installs the required 
dependencies, sets up the database in the latest version and starts the application
server for testing locally. 

You can then run the unittests locally: 

```bash
source run_tests.sh
```

You can also use the [provided Postman testsuite](MovieWorld-API-Tests.postman_collection.json) 
to test the locally running API, see description `API Tests with Postman` above.


# REST API documentation

The API is served from the base URL `/api/v1`. All endpoints that require authentication expect a JWT in the `Authorization` header with the `Bearer` scheme.

---

## Movies

### GET /movies

*   **Description**: Retrieves a paginated list of all movies.
*   **Permissions**: `get:movie` (Casting Assistant, Casting Director, Executive Producer)
*   **Query Parameters**:
    *   `page` (optional, integer): The page number to retrieve. Defaults to `1`.
    *   `per_page` (optional, integer): The number of movies per page. Defaults to `10`.
*   **Success Response (200 OK)**:
    ```json
    {
        "success": true,
        "movies": [
            {
                "id": 1,
                "title": "Inception",
                "release_date": "2010-07-16"
            }
        ],
        "total_movies": 20,
        "current_page": 1,
        "total_pages": 2
    }
    ```
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `404 Not Found`: If the requested `page` does not exist.

### POST /movies

*   **Description**: Creates a new movie.
*   **Permissions**: `add:movie` (Executive Producer)
*   **Request Body**:
    ```json
    {
        "title": "The Matrix",
        "release_date": "1999-03-31"
    }
    ```
*   **Success Response (200 OK)**: Returns the newly created movie object.
    ```json
    {
        "success": true,
        "id": 42,
        "title": "The Matrix",
        "release_date": "1999-03-31"
    }
    ```
*   **Failure Responses**:
    *   `400 Bad Request`: If `title` or `release_date` are missing or invalid.
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `add:movie` permission.

### GET /movies/{movie_id}

*   **Description**: Retrieves the details of a specific movie.
*   **Permissions**: `get:movie` (Casting Assistant, Casting Director, Executive Producer)
*   **Success Response (200 OK)**:
    ```json
    {
        "success": true,
        "id": 42,
        "title": "The Matrix",
        "release_date": "1999-03-31"
    }
    ```
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `404 Not Found`: If no movie with the given `movie_id` exists.

### PATCH /movies/{movie_id}

*   **Description**: Updates a movie's details. At least one field must be provided.
*   **Permissions**: `modify:movie` (Casting Director, Executive Producer)
*   **Request Body**:
    ```json
    {
        "title": "The Matrix (Director's Cut)",
        "release_date": "1999-04-01"
    }
    ```
*   **Success Response (200 OK)**: Returns the updated movie object.
*   **Failure Responses**:
    *   `400 Bad Request`: If the request body is empty or contains invalid data (e.g., empty title).
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `modify:movie` permission.
    *   `404 Not Found`: If no movie with the given `movie_id` exists.

### DELETE /movies/{movie_id}

*   **Description**: Deletes a movie and all associated roles.
*   **Permissions**: `delete:movie` (Executive Producer)
*   **Success Response (204 No Content)**: An empty response body.
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `delete:movie` permission.
    *   `404 Not Found`: If no movie with the given `movie_id` exists.

---

## Actors

### GET /actors

*   **Description**: Retrieves a paginated list of all actors.
*   **Permissions**: `get:actor` (Casting Assistant, Casting Director, Executive Producer)
*   **Query Parameters**:
    *   `page` (optional, integer): The page number to retrieve. Defaults to `1`.
    *   `per_page` (optional, integer): The number of actors per page. Defaults to `10`.
*   **Success Response (200 OK)**:
    ```json
    {
        "success": true,
        "actors": [
            {
                "id": 1,
                "name": "Keanu Reeves",
                "birth_date": "1964-09-02"
            }
        ],
        "total_actors": 50,
        "current_page": 1,
        "total_pages": 5
    }
    ```
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `404 Not Found`: If the requested `page` does not exist.

### POST /actors

*   **Description**: Creates a new actor.
*   **Permissions**: `add:actor` (Casting Director, Executive Producer)
*   **Request Body**:
    ```json
    {
        "name": "Morgan Freeman",
        "birth_date": "1937-06-01"
    }
    ```
*   **Success Response (200 OK)**: Returns the newly created actor object.
*   **Failure Responses**:
    *   `400 Bad Request`: If `name` or `birth_date` are missing or invalid.
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `add:actor` permission.

### DELETE /actors/{actor_id}

*   **Description**: Deletes an actor. The actor cannot be deleted if they are assigned to any roles.
*   **Permissions**: `delete:actor` (Casting Director, Executive Producer)
*   **Success Response (204 No Content)**: An empty response body.
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `delete:actor` permission.
    *   `404 Not Found`: If no actor with the given `actor_id` exists.
    *   `409 Conflict`: If the actor is currently assigned to one or more roles.

---

## Roles

Roles are sub-resources of movies.

### GET /movies/{movie_id}/roles

*   **Description**: Retrieves a paginated list of all roles for a specific movie.
*   **Permissions**: `get:movie` (Casting Assistant, Casting Director, Executive Producer)
*   **Success Response (200 OK)**:
    ```json
    {
        "success": true,
        "roles": [
            {
                "id": 101,
                "character": "Neo",
                "movie_id": 42,
                "actor_id": 1
            }
        ],
        "total_roles": 1,
        "current_page": 1,
        "total_pages": 1
    }
    ```
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `404 Not Found`: If no movie with the given `movie_id` exists.

### POST /movies/{movie_id}/roles

*   **Description**: Creates a new role for a movie. The role can be created without an actor assigned.
*   **Permissions**: `modify:movie` (Casting Director, Executive Producer)
*   **Request Body**:
    ```json
    {
        "character": "Neo",
        "actor_id": 1 // Optional
    }
    ```
*   **Success Response (200 OK)**: Returns the newly created role object.
*   **Failure Responses**:
    *   `400 Bad Request`: If `character` is missing or invalid.
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `modify:movie` permission.
    *   `404 Not Found`: If the `movie_id` or `actor_id` (if provided) does not exist.
    *   `409 Conflict`: If a role with the same character name already exists for this movie.

### PATCH /movies/{movie_id}/roles/{role_id}

*   **Description**: Updates a role's details, such as changing the character name or assigning/unassigning an actor.
*   **Permissions**: `modify:movie` (Casting Director, Executive Producer)
*   **Request Body**:
    ```json
    {
        "character": "Neo (The One)",
        "actor_id": 1
    }
    ```
*   **Success Response (200 OK)**: Returns the updated role object.
*   **Failure Responses**:
    *   `400 Bad Request`: If the request body is empty or contains invalid data.
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `modify:movie` permission.
    *   `404 Not Found`: If the `movie_id`, `role_id`, or `actor_id` (if provided) does not exist.

### DELETE /movies/{movie_id}/roles/{role_id}

*   **Description**: Deletes a specific role from a movie.
*   **Permissions**: `modify:movie` (Casting Director, Executive Producer)
*   **Success Response (204 No Content)**: An empty response body.
*   **Failure Responses**:
    *   `401 Unauthorized`: If the `Authorization` header is missing or invalid.
    *   `403 Forbidden`: If the user's role does not have the `modify:movie` permission.
    *   `404 Not Found`: If the `movie_id` or `role_id` does not exist.
