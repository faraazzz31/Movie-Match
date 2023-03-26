"""
CSC11 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""

from __future__ import annotations
import csv
import pandas
from typing import Optional

#TODO: add pythonta and pytest
#Christoffer: Graph class, RI, recommendations
#Faraaz: create_graph, RI, UI
#Razan: calculate_similarity, arrange_cosine_similarities

movie_title_mapping = {} #mapping of movie title to Movie Vertex

class User:
    """
    User class where each user acts as a Vertex in the graph.

    Instance Attributes:
    - user_id:
        The unique id of the user.
    - movies:
        The mapping of movies the user has watched where all keys are the movies and the corresponding values are
        the ratings.

    Representation Invariants:
    ...
    """
    user_id: int
    movies: dict[Movie, float]

    def __init__(self, user_id: int):
        self.user_id = user_id


class Movie:
    """
        Movie class where each movie acts as a Vertex in the graph.

        Instance Attributes:
        - movie_id:
            The unique id of the user.
        - users:
            The mapping of users who have watched the movie where all keys are the users and the corresponding values
            are the ratings provided by the users.
        - title:
            The name of the movie.

        Representation Invariants:
        ...
        """
    movie_id: int
    users: dict[User, float]
    title: str

    def __init__(self, user_id: int, title: str):
        self.user_id = user_id
        self.title = title


class RatingGraph:
    """
    A class for a recommender system that acts like a graph where users are linked to movies with
    edges having the rating.

    Private Instance Attributes:
        -_users:
            A mapping of users where the keys are the user_id and the values are the corresponding User Vertex.
        -_movies:
            A mapping of movies where the keys are the movie_id and the values are the corresponding Movie Vertex.

    Representation Invariants:
    ...
    """
    _users: dict[int, User]
    _movies: dict[int, Movie]

    def __init__(self):
        """initialize an empty RatingGraph"""
        self._users = {}
        self._movies = {}

    def add_users(self, user_id: int) -> None:
        ...

    def add_movies(self, movie_id: int, title: str) -> None:
        ...

    def add_edge(self, user_id: int, movie_id: int, rating: float) -> None:
        user = ...
        movie = ...
        user[movie] = rating
        movie[user] = rating

def create_graph(csv_file_user: csv, csv_file_movie: csv) -> RatingGraph:
    """
    1. We add all the movies to the graph (movies node)
    2. Access the users dataset
    3. If the user is not in the graph -> we add the users (user_id)
    4. Add the edge(user_id, movie_id, rating)
    5. update movie_title_mapping = {} #mapping of movie title to Movie Vertex
    """
    ...

def compute_cosine_similarity(movie1: Movie, movie2: Movie, graph: RatingGraph) -> Optional[float]:
    """return None if only 1 or 0 user watched movie1 and movie2"""
    ...

def arrange_cosine_similarities() -> list[tuple[float, str]]:
    """ return list of tuple in the form (cosine similarity, movie title)
    Arrange all the cosine similarities.
    If cosine similarity is none do not add to the tuple."""
    # graph = create_graph()
    ...

def recommendations(watched_movies: list[str]) -> list[str]:
    ...
