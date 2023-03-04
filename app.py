import pickle
import streamlit as st
import requests

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon=":movie_camera:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center; color: orange;'>Movie Recommender System</h1>", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

@st.cache(allow_output_mutation=True)
def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

movies = load_pickle('model/movie_list.pkl')
similarity = load_pickle('model/similarity.pkl')

# Add a dropdown to select a movie and a button to show recommendations.
selected_movie = st.selectbox("Select a movie to see recommendations", movies['title'].values)
if st.button('Show recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

# Add a link to the creator's LinkedIn profile.
st.markdown("<p style='text-align: right;'>Created by <a href='https://www.linkedin.com/in/pratul-goyal-7a7229119/'>Pratul Goyal</a></p>", unsafe_allow_html=True)
