# Fetch the neccesary python modules
import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image


# Recommend movies based on content
def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    # Fetch the posters for each recommended movie
    for  i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster

# Load the necessary python pickle files
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))   


# Fetch posters from the TMDb database
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3395f31d64bb6284ad9b4079db06dd21&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Web app's hero section - Display Title, Dropdown
st.title("Movie Recommender System")

#Add image
image_url = 'https://raw.githubusercontent.com/SatyamedhasP/Movie_Recommender__System/main/Image.jpg'
image = Image.open(requests.get(image_url, stream=True).raw)
st.image(image, use_column_width=True)

selected_movie_name = st.selectbox(
'Select a movie to recommend',
movies['original_title'].values)

# Output recommendations with posters
if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)
 
    col1, col2, col3, col4,  col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])