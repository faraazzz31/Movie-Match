# MovieMatch - Movie Recommendation System

A Python-based movie recommendation system that leverages community-sourced reviews and implements graph algorithms with cosine similarity for personalized movie suggestions. The system combines content-based and collaborative filtering techniques to generate accurate recommendations based on user preferences and movie genres.

## Features
- Uses MovieLens dataset with 100,000 ratings from 600 users across 9,000 movies
- Implements graph-based recommendation algorithm using cosine similarity
- Combines content-based filtering (movie genres) and collaborative filtering (user ratings)
- Interactive GUI for easy movie search and recommendation generation
- Provides personalized recommendations based on up to 3 favorite movies

## Tech Stack
- Python
- Pandas for data processing
- Tkinter for GUI

## Installation
1. Clone the repository
2. Extract the datasets folder to the same location as the source files
3. Ensure all required files are present:
   - main.py
   - rating_graph.py
   - gui.py
   - recommender.py
   - datasets/movies.csv
   - datasets/ratings.csv

## Usage
1. Run `main.py`
2. Enter three movies in the search boxes
3. Click "Get Recommendations!" to generate personalized movie suggestions
4. Use the "Delete" button to clear recommendations and start over

## Dataset
Uses the MovieLens "Latest Datasets" (small version) which includes movies released up to 2018. The dataset provides:
- Movie information (ID, title, genres)
- User ratings (UserID, MovieID, Rating)
