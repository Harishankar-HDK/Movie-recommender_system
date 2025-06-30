import streamlit as st
import pickle
import requests #It is a library used when we are using API keys
from dotenv import load_dotenv #Its a library that help to get the API key from the .env file
import os


load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


def app():
    def fetch_poster(movie_title):
        response =  requests.get(f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}") 
        data = response.json() #We convert the result into json file to take the path of the poster

        # Check if the response contains 'Poster' and it's not 'N/A'
        if data.get('Poster') and data['Poster'] != "N/A":
            return data['Poster'] #It will return the value of the key 'Poster' which is the location to the image of the poster
        else:
            # Return a placeholder image URL if poster is missing or not available
            return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg" #This will display a no image poster if there is no image for a poster

    def recommend(movies): #Same function we written in the jupyter notebook
        movies_index = movies_dataframe[movies_dataframe['title'] == movies].index[0]
        distances = similarity[movies_index]
        movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

        recommend_movies = []
        recommended_movies_poster = [] #We have created a new list to append the poster that we fetch from the fetch_poster function using API
        
        for i in movie_list:
            recommend_movies.append(movies_dataframe.iloc[i[0]].title)
            
            #Fetch poster from the API 
            recommended_movies_poster.append(fetch_poster(movies_dataframe.iloc[i[0]].title)) #Here we are passing movie title to the fetch_poster function
            #IF any error occur check here
        return recommend_movies,recommended_movies_poster



    st.title("Movie Recommender System")

    movies_dataframe = pickle.load(open('movies1.pkl','rb')) #Pickle will help to open the dataframe we stored as pickle file in the jupyter notebook and rb represent read binary
    #In the movies.pkl we have only passed the dataframe we have created that is new_df dataframe we have created in the jupyter notebook

    movies_list= movies_dataframe['title'].values 
    #This will returns all names of the movie that comes under the column title movies['title'] will give the name of the movie and index but we need only the name of the movie thats why we have used movie_list['title'].values

    similarity = pickle.load(open('similarity1.pkl','rb'))

    selected_movie = st.selectbox(
        "Which movie you would like to select?",
        (movies_list),
        index=None,
        placeholder='Enter the movie you like...',
    )


    if st.button("Recommend"):
        name,posters = recommend(selected_movie) 
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"<p style='font-size:16px; font-weight:bold'>{name[0]}</p>", unsafe_allow_html=True)
            st.image(posters[0])
        with col2:
            st.markdown(f"<p style='font-size:16px; font-weight:bold'>{name[1]}</p>", unsafe_allow_html=True)
            st.image(posters[1])
        with col3:
            st.markdown(f"<p style='font-size:16px; font-weight:bold'>{name[2]}</p>", unsafe_allow_html=True)
            st.image(posters[2])
        with col4:
            st.markdown(f"<p style='font-size:16px; font-weight:bold'>{name[3]}</p>", unsafe_allow_html=True)
            st.image(posters[3])
        with col5:
            st.markdown(f"<p style='font-size:16px; font-weight:bold'>{name[4]}</p>", unsafe_allow_html=True)
            st.image(posters[4])

    if st.button("Sign out"):
        st.session_state.signed_in = False
        st.session_state.user = None
        st.rerun()

    

