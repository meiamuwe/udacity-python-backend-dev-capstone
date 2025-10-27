import os
import uuid
from .helper import format_date
from flask_sqlalchemy import SQLAlchemy


"""
Get and (if required) correct the database URL
from the environment.
"""
database_path = os.environ["DATABASE_URL"]
if database_path and database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


# Model definition
"""
Model class to represent a movie.
Movies have an id, a title and a release date.
"""


class Movie(db.Model):
    """Model class for movies."""

    __tablename__ = "movie"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # One-to-many relations to movies
    roles = db.relationship(
        "Role", backref="movie", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": format_date(self.release_date),
        }


"""
Model class to represent a role.
Roles have an id, a character and an optional actor.
"""


class Role(db.Model):
    """Model class for roles."""

    __tablename__ = "role"
    __table_args__ = (
        db.UniqueConstraint(
            "movie_id", "character", name="_role_movie_id_character_uc"
        ),
    )

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    character = db.Column(db.String(100), nullable=False)
    movie_id = db.Column(
        db.String(36),
        db.ForeignKey("movie.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    actor_id = db.Column(
        db.String(36),
        db.ForeignKey("actor.id", ondelete="RESTRICT"),
        nullable=True,
    )

    def __init__(self, character, movie, actor=None):
        self.character = character
        self.movie = movie
        self.actor = actor

    def format(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "character": self.character,
            "actor_id": self.actor_id,
        }


"""
Model class to represent an actor.
Actors have an id, a name and a birth date.
"""


class Actor(db.Model):
    """Model class for actors."""

    __tablename__ = "actor"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    # One-to-many relationship to Role.
    roles = db.relationship(
        "Role", backref="actor", passive_deletes=True, lazy="dynamic"
    )

    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": format_date(self.birth_date),
        }
