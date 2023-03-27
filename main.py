"""
CSC11 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""

from __future__ import annotations
import csv
import pandas
from typing import Optional

#TODO: add pythonta and pytest, and rewrite the docstring and precondition
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
    - all(0.0 <= self.movies[movie] <= 5.0 for movie in self.movies)
    - all(self in movie.users for movie in self.movies)
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
        - all(0.0 <= self.users[user] <= 5.0 for user in self.users)
        - all(self in user.movies for user in self.users)
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
        """Add a new user with the given id to this graph.

        If the user has already been in the graph, do not add the user.
        """
        if user_id in self._users:
            return

        new_user = User(user_id)
        self._users[user_id] = new_user


    def add_movies(self, movie_id: int, title: str) -> None:
        """Add a new movie with the given id and title to this graph.

        If the movie has already been in the graph, do not add the movie.
        """
        if movie_id in self._movies:
            return

        new_movie = Movie(movie_id, title)
        self._movies[movie_id] = new_movie


    def add_edge(self, user_id: int, movie_id: int, rating: float) -> None:
        """Add a new edge between a user and a movie with the rating given as the weight.

        If the given user_id or movie_id do not correspond to a node in this graph, raise ValueError
        """
        if not (user_id in self._users and movie_id in self._movies):
            raise ValueError
        
        user = self._users[user_id]
        movie = self._movies[movie_id]
        
        user.movies[movie] = rating
        movie.users[user] = rating

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
    """Give five movies recommendation based on the given three watched_movies using cosine similarity.

    Based on the pre-computed cosine similarity, the recommender system will recommend movies according these following
    steps:
    1. For each watched_movies take the 5 most similar movies.
    2. Choose 5 random movies from the pool of similar movies.
    3. If there is at least one movie in the movies recommendation that has been watched by the user,
    then take the next 5 most similar movies and return to step 2.

    Should we use graph as the parameter?? and remove the movie_title_mapping dict


    Preconditions:
    - len(watched_movies) == 3
    """
    graph = create_graph("ratings.csv", "movies.csv")

    similar_movies = []

    i = 0
    while True:
        for watched_movie in watched_movies:
            watched_movie_node = movie_title_mapping[watched_movie]
            similar_movies.extend((arrange_cosine_similarities(watched_movie_node, graph))[i:(i + 5)])

        chosen_movies = sample(similar_movies, 5)
        if valid(chosen_movies, watched_movies):
            return [movie[1] for movie in chosen_movies]

        i += 5

def valid(chosen_movies: list[tuple[float, str]], watched_movies: list[str]) -> bool:
    """Return false if at least one of chosen_movies has been watched by the user"""

    for rating, title in chosen_movies:
        if title in watched_movies:
            return False

    return True
