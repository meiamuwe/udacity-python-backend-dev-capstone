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

The test suite is set up for local test and requires the definition of the following variables
before executing the tests: 

| Variable | Purpose | Values  |
|----------|---------|---------|
| `baseUrl` | URL for the server, that runs the API | Default value `http://localhost:5000` is suitable for local development. To test the production deployment, please use `https://movieworld-udacity-capstone.onrender.com` instead. |
| `auth0_client_id` | Auth0 client ID | You can find the required value in the project submission comments.|
| `auth0_client_secret` | Auth0 client secret | You can find the required value in the project submission comments.|



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

Execute the following commands to set up the database user and database. 

```
psql --username=postgres -a -f movieworld_db_test.sql
psql --username movieworld_test movieworld_test

Enter password: movieworld_test


If you want some example data, you can use

```
psql --username=movieworld_test -a -f movieworld_db_content.sql

Enter password: movieworld_test

```



# Instructions 

# External authentication and roles





## Sample login page at `Auth0`



To simulate a login with these users, you can use:
*  [Login when running the application locally](http://localhost:5000/)
*  [Login for the deployed application](https://movieworld-udacity-capstone.onrender.com/)


# TODO: RUBICS

Document project description in README file, including the following information:
* Motivation for the project
* URL location for the hosted API
* Project dependencies, local development and hosting instructions,
* Detailed instructions for scripts to set up authentication, install any project dependencies and run the development server.
* Documentation of API behavior and RBAC controls
