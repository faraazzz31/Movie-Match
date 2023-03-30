"""
CSC11 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""

from __future__ import annotations
import csv
import pandas
from typing import Optional
import tkinter as tk
from random import sample

# TODO: add pythonta and pytest, and rewrite the docstring and precondition
# Christoffer: Graph class, RI, recommendations
# Faraaz: create_graph, RI, UI
# Razan: calculate_similarity, arrange_cosine_similarities

movie_title_mapping = {}    # mapping of movie title to Movie Vertex
movie_title_name_list = []


class User:
    """User class where each user acts as a Vertex in the graph.

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
        self.movies = {}


class Movie:
    """Movie class where each movie acts as a Vertex in the graph.
    Instance Attributes:
    - movie_id:
        The unique id of the user.
    - users:
        The mapping of users who have watched the movie where all keys are the users and the corresponding values
        are the ratings provided by the users.
    - title:
        The name of the movie.
    - genre:
        The genre of the movie
    Representation Invariants:
    - all(0.0 <= self.users[user] <= 5.0 for user in self.users)
    - all(self in user.movies for user in self.users)
    """
    movie_id: int
    users: dict[User, float]
    title: str
    genre: str

    def __init__(self, movie_id: int, title: str, genre: str):
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
    Representation Invariants:
    ...
    """
    _users: dict[int, User]
    _movies: dict[int, Movie]

    def __init__(self):
        """Initialize an empty RatingGraph"""
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

    def get_movie(self, movie_id) -> Movie:
        """Based on the movie_id, return the movie node.
        Preconditions:
        - movie_id in self._movies
        """
        return self._movies[movie_id]

    def get_all_movies(self) -> list[Movie]:
        """Returns a list of all movies added to the graph.
        Preconditions:
        ...
        """
        return list(self._movies.values())


def create_graph(csv_file_user: csv, csv_file_movie: csv) -> RatingGraph:
    """
    1. We add all the movies to the graph (movies node)
    2. Access the users dataset
    3. If the user is not in the graph -> we add the users (user_id)
    4. Add the edge(user_id, movie_id, rating)
    5. update movie_title_mapping = {} #mapping of movie title to Movie Vertex
    """
    graph = RatingGraph()
    movie_file = pandas.read_csv(csv_file_movie)
    user_file = pandas.read_csv(csv_file_user)

    for i in movie_file.index:
        graph.add_movies(int(movie_file["movieId"][i]), str(movie_file["title"][i]))
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


def arrange_cosine_similarities(movie1: Movie, graph: RatingGraph) -> list[tuple[float, str]]:
    """
    Using the movie and the graph, return list of tuple in the form (cosine similarity, movie title)
    Arrange all the cosine similarities.
    If cosine similarity is none do not add to the tuple.
    """
    res = []
    movie_list = graph.get_all_movies()
    for movie2 in movie_list:
        cosine_similarity = compute_cosine_similarity(movie1, movie2)
        if cosine_similarity is not None:
            res.append((cosine_similarity, movie2.title))
    res.sort(key=lambda x: x[0])
    return res


def recommendations(watched_movies: list[str]) -> list[str]:
    """Give five movies recommendation based on the given three watched_movies using cosine similarity.
    Based on the pre-computed cosine similarity, the recommender system will recommend movies according these following
    steps:
    1. For each watched_movies take the most similar movies.
    2. If there is at least one movie in the movies recommendation that has been watched by the user,
    then take the next most similar movies for each watched_movies
    3. Else we return that three similar movies.
    Preconditions:
    - len(watched_movies) == 3
    """
    graph = create_graph("ratings.csv", "movies.csv")

    similar_movies = []

    i = 0
    while True:
        for watched_movie in watched_movies:
            watched_movie_node = movie_title_mapping[watched_movie]
            similar_movies.extend((arrange_cosine_similarities(watched_movie_node, graph))[i:i+1])

        if valid(similar_movies, watched_movies):
            return [movie[1] for movie in similar_movies]

        i += 1


def valid(chosen_movies: list[tuple[float, str]], watched_movies: list[str]) -> bool:
    """Return false if at least one of chosen_movies has been watched by the user"""

    for rating, title in chosen_movies:
        if title in watched_movies:
            return False

    return True


# UI Part
root = tk.Tk()
root.title("Movie Match")
root.geometry("800x800")
create_graph("ratings.csv", "movies.csv")
root.configure(bg="#AEC2B9")
widget = 0


def on_select(event):
    """Store which widget is being selected in the widget variable"""

    global widget
    widget = event.widget.extra


def listbox_update(movies: list) -> None:
    """Update the listbox with the list of movies"""

    list_box.delete(0, tk.END)
    for movie in movies:
        list_box.insert(tk.END, movie)


def fill_listbox(event) -> None:
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


def search(event) -> None:
    """Show predicted search outcomes in the list box.
    If the entry box is empty, reset the list box to all the movies.
    """

    if widget == "entry1":
        typed = input_box1.get()
        if typed == '':
            movies = movie_title_name_list
        else:
            movies = []
            for movie in movie_title_name_list:
                if typed.lower() in movie.lower():
                    movies.append(movie)
        listbox_update(movies)

    elif widget == "entry2":
        typed = input_box2.get()
        if typed == '':
            movies = movie_title_name_list
        else:
            movies = []
            for movie in movie_title_name_list:
                if typed.lower() in movie.lower():
                    movies.append(movie)
        listbox_update(movies)

    elif widget == "entry3":
        typed = input_box3.get()
        if typed == '':
            movies = movie_title_name_list
        else:
            movies = []
            for movie in movie_title_name_list:
                if typed.lower() in movie.lower():
                    movies.append(movie)
        listbox_update(movies)


def submit():
    """Collect the user input of the movies and show the recommendations"""

    first = input_box1.get()
    second = input_box2.get()
    third = input_box3.get()
    movie_list = [first] + [second] + [third]
    print(movie_list)
    movie_rec = recommendations(movie_list)
    movie_text.configure(state="normal")
    for x in movie_rec:
        movie_text.insert(tk.END, x + '\n')
    movie_text.configure(state="disabled")


def delete_text():
    """Delete the text from the text box"""
    
    movie_text.configure(state="normal")
    movie_text.delete(1.0, tk.END)
    movie_text.configure(state="disabled")


header = tk.Label(root, text="Movie Match", font=("Marker Felt", 45), bg="#AEC2B9", fg="black")
header.pack(pady=5)

instructions = tk.Label(root, text="Please Enter Three Movies That You Have Enjoyed Watching", font=("PT Sans", 15), bg="#AEC2B9", fg="black")
instructions.pack(pady=5)

input_box1 = tk.Entry(root, font=("PT Sans", 15), width=40, bg="#F2F8F3", fg="black")
input_box1.extra = "entry1"
input_box1.pack(pady=12)

input_box2 = tk.Entry(root, font=("PT Sans", 15), width=40, bg="#F2F8F3", fg="black")
input_box2.extra = "entry2"
input_box2.pack(pady=12)

input_box3 = tk.Entry(root, font=("PT Sans", 15), width=40, bg="#F2F8F3", fg="black")
input_box3.extra = "entry3"
input_box3.pack(pady=12)

list_box = tk.Listbox(root, width=60, height=10, font=("PT Sans", 15), bg="#F2F8F3", fg="black")
list_box.extra = "box"
list_box.pack(pady=20)

button = tk.Button(root, text="Get Recommendations!", command=submit, bg="#F2F8F3", fg="black")
button.pack()

movie_text = tk.Text(root, height=15, bg="#F2F8F3", fg="black")
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
