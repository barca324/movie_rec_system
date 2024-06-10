from flask import Flask, render_template, request
import pickle
import pandas as pd
import imdb
import json
import requests
ia=imdb.IMDb()
app = Flask(__name__)

# Load data
movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_movie_poster(imdb_id):
    ia = imdb.IMDb()

    # Get movie details from the OMDB API using IMDb ID
    omdb_api_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=75e51c41"
    response = requests.get(omdb_api_url)
    response=response.text
    return response

    # Extract poster URL from movie data
    

    
   
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_value = request.form.get('selected_value')
        poster_url_final=[]
        data=[]
        images=[]
        
        recommendations,poster_url = recommend(selected_value)
        for i in poster_url:
            poster_url_final.append(get_movie_poster(i))
        for i in poster_url_final:
            data.append(json.loads(i))
        for i in data:
            images.append(i['Poster'])
        
        image_detail=dict(zip(recommendations,images))
        print(image_detail)
        return render_template('index.html', options=movies['original_title'].values.tolist(), selected_value=selected_value, recommendations=recommendations,image_detail=image_detail)
    else:
        options = movies['original_title'].values.tolist()
        return render_template('index.html', options=options)

def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    poster_url=[]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]]['original_title'])
        poster_url.append(movies.iloc[i[0]]['imdb_id'])
    print(poster_url)
    return recommended_movies,poster_url

if __name__ == '__main__':
    app.run(debug=True)
