"""
CSC111 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""

from __future__ import annotations
import csv
import pandas
from typing import Optional
import tkinter as tk
from random import sample

movie_title_mapping = {}  # mapping of movie title to Movie Vertex
movie_title_name_list = []


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

    def get_movie(self, movie_id) -> Movie:
        """Based on the movie_id, return the movie node.
        Preconditions:
        - movie_id in self._movies
        """
        return self._movies[movie_id]

    def get_all_movies(self) -> list[Movie]:
        """Returns a list of all movies added to the graph.
        """
        return list(self._movies.values())


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
        norm1 = sum([ratings1[i] ** 2 for i in range(0, len(ratings1))]) ** 0.5
        norm2 = sum([ratings2[i] ** 2 for i in range(0, len(ratings2))]) ** 0.5
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
                        not ((recommended_movies[i][1] in similar_movies) or (
                                recommended_movies[i][1] in watched_movies)):
                    similar_movies.append(recommended_movies[i][1])
                    j += 1

                i += 1

    return sample(similar_movies, 5)


root = tk.Tk()
root.title("Movie Match")
root.geometry("1000x1000")
create_graph("datasets/ratings.csv", "datasets/movies.csv")
root.configure(bg="#AEC2B9")
widget = 0


def on_select(event):
    """Store which widget is being selected in the widget variable"""

    global widget
    widget = event.widget.extra


def listbox_update(movies: list):
    """Update the listbox with the list of movies"""

    list_box.delete(0, tk.END)
    for movie in movies:
        list_box.insert(tk.END, movie)


def fill_listbox(event):
    """Fill the entry box with the movie selected from the list box"""

    if widget == "entry1":
        input_box1.delete(0, tk.END)
        input_box1.insert(0, list_box.get(tk.ANCHOR))

    elif widget == "entry2":
        input_box2.delete(0, tk.END)
        input_box2.insert(0, list_box.get(tk.ANCHOR))

    elif widget == "entry3":
        input_box3.delete(0, tk.END)
        input_box3.insert(0, list_box.get(tk.ANCHOR))


def search(event):
    """Show predicted search outcomes in the list box.
    If the entry box is empty, reset the list box to all the movies.
    """

    if widget == "entry1":
        entered = input_box1.get()
        if entered == '':
            movies = movie_title_name_list
        else:
            movies = []
            for movie in movie_title_name_list:
                if entered.lower() in movie.lower():
                    movies.append(movie)
        listbox_update(movies)

    elif widget == "entry2":
        entered = input_box2.get()
        if entered == '':
            movies = movie_title_name_list
        else:
            movies = []
            for movie in movie_title_name_list:
                if entered.lower() in movie.lower():
                    movies.append(movie)
        listbox_update(movies)

    elif widget == "entry3":
        entered = input_box3.get()
        if entered == '':
            movies = movie_title_name_list
        else:
            movies = []
            for movie in movie_title_name_list:
                if entered.lower() in movie.lower():
                    movies.append(movie)
        listbox_update(movies)


def submit():
    """Collect the user input of the movies"""

    first = input_box1.get()
    second = input_box2.get()
    third = input_box3.get()
    movie_list = [first] + [second] + [third]
    if '' in movie_list:
        lb = tk.Label(root, text="Please Enter Three Movies", font=("PT Sans", 15), bg="#AEC2B9", fg="red")
        lb.pack()
    else:
        movie_rec = recommendations(movie_list)
        movie_text.configure(state="normal")
        for x in movie_rec:
            movie_text.insert(tk.END, x + '\n')
        movie_text.configure(state="disabled")


def delete_text():
    """Remove all the text inside the recommendation text box"""
    movie_text.configure(state="normal")
    movie_text.delete(1.0, tk.END)
    movie_text.configure(state="disabled")


header = tk.Label(root, text="Movie Match", font=("Marker Felt", 45), bg="#AEC2B9", fg="black")
header.pack(pady=5)

instructions = tk.Label(root, text="Please Enter Three Movies That You Have Enjoyed Watching", font=("PT Sans", 15),
                        bg="#AEC2B9", fg="black")
instructions.pack(pady=5)

instructions2 = tk.Label(root,
                         text="Start by typing the movie in the entry box then selecting it from the list box below",
                         font=("PT Sans", 15), bg="#AEC2B9", fg="black")
instructions2.pack()

input_box1 = tk.Entry(root, font=("PT Sans", 15), width=40, bg="#F2F8F3", fg="black")
input_box1.extra = "entry1"
input_box1.pack(pady=12)

input_box2 = tk.Entry(root, font=("PT Sans", 15), width=40, bg="#F2F8F3", fg="black")
input_box2.extra = "entry2"
input_box2.pack(pady=12)

input_box3 = tk.Entry(root, font=("PT Sans", 15), width=40, bg="#F2F8F3", fg="black")
input_box3.extra = "entry3"
input_box3.pack(pady=10)

list_box = tk.Listbox(root, width=60, height=6, font=("PT Sans", 15), bg="#F2F8F3", fg="black")
list_box.extra = "box"
list_box.pack(pady=12)

button = tk.Button(root, text="Get Recommendations!", command=submit, bg="#F2F8F3", fg="black")
button.pack()

movie_text = tk.Text(root, font=("PT Sans", 15), height=10, bg="#F2F8F3", fg="black")
movie_text.pack(pady=10)

delete = tk.Button(root, text='Delete', command=delete_text, bg="#F2F8F3", fg="black")
delete.pack(pady=10)

listbox_update(movie_title_name_list)

list_box.bind("<<ListboxSelect>>", fill_listbox)

input_box1.bind("<KeyRelease>", search)
input_box2.bind("<KeyRelease>", search)
input_box3.bind("<KeyRelease>", search)

input_box1.bind("<FocusIn>", on_select)
input_box2.bind("<FocusIn>", on_select)
input_box3.bind("<FocusIn>", on_select)

root.mainloop()

