"""
CSC111 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
Module: rating_graph.py

This module contains the RatingGraph class which is a Graph class which consists of
Movie Vertices and User Vertices and the edges represent the rating given by each user
to the corresponding movie.

This file is Copyright (c) 2023 , Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""
from __future__ import annotations


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

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.movies = {}


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
    genre: str

    def __init__(self, movie_id: int, title: str, genre: str) -> None:
        self.movie_id = movie_id
        self.title = title
        self.users = {}
        self.genre = genre


class RatingGraph:
    """
    A class for a recommender system that acts like a graph where users are linked to movies with
    edges having the rating.

    Private Instance Attributes:
        -_users:
            A mapping of users where the keys are the user_id and the values are the corresponding User Vertex.
        -_movies:
            A mapping of movies where the keys are the movie_id and the values are the corresponding Movie Vertex.
    """
    _users: dict[int, User]
    _movies: dict[int, Movie]

    def __init__(self) -> None:
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

    def add_movies(self, movie_id: int, title: str, genre: str) -> None:
        """Add a new movie with the given id, title and genre to this graph.
        If the movie has already been in the graph, do not add the movie.
        """
        if movie_id in self._movies:
            return

        new_movie = Movie(movie_id, title, genre)
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

    def get_movie(self, movie_id: int) -> Movie:
        """Based on the movie_id, return the movie node.
        Preconditions:
        - movie_id in self._movies
        """
        return self._movies[movie_id]

    def get_all_movies(self) -> list[Movie]:
        """Returns a list of all movies added to the graph.
        """
        return list(self._movies.values())


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'pandas', 'tkinter', 'random']
    })
