"""
CSC111 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
Module: recommender.py

This module contains all the functions required to create the RatingGraph from
the dataset and the calculation functions to sort the recommendations of movies
using cosine similarity.

This file is Copyright (c) 2023 , Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""
import csv
from typing import Optional
from random import sample
import pandas
from rating_graph import Movie, RatingGraph

movie_title_mapping = {}  # mapping of movie title to Movie Vertex
movie_title_name_list = []  # list of movie titles


def find_genre(genres: str) -> str:
    """return the main genre of the movie"""
    mov_genre = genres
    if "|" in genres:
        x = genres.split("|")
        if "Children" in x:
            mov_genre = "Children"
        elif "Animation" in x:
            mov_genre = "Animation"
        elif "Fantasy" in x:
            mov_genre = "Fantasy"
        elif "Horror" in x:
            mov_genre = "Horror"
        elif "Thriller" in x:
            mov_genre = "Thriller"
        elif "Romance" in x:
            mov_genre = "Romance"
        elif "War" in x:
            mov_genre = "War"
        else:
            mov_genre = x[0]

    return mov_genre


def create_graph(csv_file_user: csv, csv_file_movie: csv) -> RatingGraph:
    """
    Add all the Movie and User Vertices to the graph and add all the edges between them based on the ratings.
    Also update movie_title_mapping and movie_title_name_list.
    """
    graph = RatingGraph()
    movie_file = pandas.read_csv(csv_file_movie)
    user_file = pandas.read_csv(csv_file_user)

    for i in movie_file.index:
        graph.add_movies(int(movie_file["movieId"][i]), str(movie_file["title"][i]),
                         find_genre(str(movie_file["genres"][i])))
        movie_title_mapping[str(movie_file["title"][i])] = graph.get_movie(int(movie_file["movieId"][i]))
        if str(movie_file["title"][i]) not in movie_title_name_list:
            movie_title_name_list.append(str(movie_file["title"][i]))

    for j in user_file.index:
        graph.add_users(int(user_file["userId"][j]))
        graph.add_edge(int(user_file["userId"][j]), int(user_file["movieId"][j]), float(user_file["rating"][j]))

    return graph


def compute_cosine_similarity(movie1: Movie, movie2: Movie) -> Optional[float]:
    """Returns the cosine similarity value between two movies.
    Returns None if only 1 or 0 user watched movie1 and movie2, or if the two movies are the same.
    Preconditions:
    - movie1.users != {} and movie2.users != {}
    """
    if movie1 is movie2:
        return None

    ratings1, ratings2 = [], []
    for user in movie1.users:
        if user in movie2.users:
            ratings1.append(movie1.users[user])
            ratings2.append(movie2.users[user])

    if len(ratings1) < 2:
        return None
    else:
        dot_product = sum([ratings1[i] * ratings2[i] for i in range(0, len(ratings1))])
        norm1 = sum([rating ** 2 for rating in ratings1]) ** 0.5
        norm2 = sum([rating ** 2 for rating in ratings2]) ** 0.5
        return dot_product / (norm1 * norm2)


def arrange_cosine_similarities(movie1: Movie, graph: RatingGraph, compare_genre: bool) -> list[tuple[float, str]]:
    """
    Using the movie and the graph, return list of tuple in the form (cosine similarity, movie title)
    Arrange all the cosine similarities.
    If cosine similarity is none do not add to the tuple.
    Pass in a bool variable `compare_genre`. If `compare_genre` is True, then we compare only with movies with similar
    genre.
    If `compare_genre` is False, then we don't compare the genres.
    """
    res = []
    movie_list = graph.get_all_movies()
    for movie2 in movie_list:
        if compare_genre and movie1.genre != movie2.genre:
            continue

        cosine_similarity = compute_cosine_similarity(movie1, movie2)
        if cosine_similarity is not None:
            res.append((cosine_similarity, movie2.title))
    res.sort(key=lambda x: x[0])
    return res


def recommendations(watched_movies: list[str]) -> list[str]:
    """Give five movies recommendation based on the given three watched_movies using cosine similarity.
    Based on the genre of the movie and cosine similarity, the recommender system will recommend movies according these
    following steps:
    1. For every movie that a random user likes, the system will select the top five movies that are most similar.
    These movies should have the same genre and the highest cosine similarity with the movie that the user likes.
    2. If the system does not have enough movies to recommend, it will select the top five most similar movies based
    ONLY on cosine similarity for each watched movie.
    3. Nevertheless, the recommended movies should not have been watched by the user, and they should not contain any
    duplicates.
    4. Then, from the pool of the recommended movies, the system will take five movies randomly.
    Preconditions:
    - len(watched_movies) == 3
    """

    graph = create_graph("datasets/ratings.csv", "datasets/movies.csv")

    similar_movies = []

    for watched_movie in watched_movies:
        watched_movie_node = movie_title_mapping[watched_movie]
        recommended_movies = arrange_cosine_similarities(watched_movie_node, graph, True)

        i = 0
        while i < len(recommended_movies):
            j = 0
            if j < 5 and \
                    not ((recommended_movies[i][1] in similar_movies) or (recommended_movies[i][1] in watched_movies)):
                similar_movies.append(recommended_movies[i][1])
                j += 1

            i += 1

    if len(similar_movies) < 3:
        for watched_movie in watched_movies:
            watched_movie_node = movie_title_mapping[watched_movie]
            recommended_movies = arrange_cosine_similarities(watched_movie_node, graph, False)

            i = 0
            while i < len(recommended_movies):
                j = 0
                if j < 5 and \
                        not ((recommended_movies[i][1] in similar_movies)
                             or (recommended_movies[i][1] in watched_movies)):
                    similar_movies.append(recommended_movies[i][1])
                    j += 1

                i += 1

    return sample(similar_movies, 5)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'pandas', 'tkinter', 'rating_graph', 'random'],
        'disable': ['R0912', 'E9997', 'E9992', 'R1702', 'E9970', 'E9971', 'C0103', 'W0613']
    })
