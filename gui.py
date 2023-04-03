"""
CSC111 Course Project: Movie Match (Movie Recommendation System)
Authors: Christoffer Tan, Faraaz Ahmed, Razan Rifandi
Module: gui.py

This module contains all the functions necessary to create an interactive user
interface for the movie recommendation system. It includes code for three entry
boxes, two buttons, one list box and one text box, alongside algorithms to update
the list box as the user types a movie in the entry box.

This file is Copyright (c) 2023 , Christoffer Tan, Faraaz Ahmed, Razan Rifandi
"""
import tkinter as tk
from recommender import create_graph, movie_title_name_list, recommendations

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

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'pandas', 'tkinter', 'random', 'recommender'],
        'disable': ['R0912', 'E9997', 'E9992', 'R1702', 'E9970', 'E9971', 'C0103', 'W0613']
    })
