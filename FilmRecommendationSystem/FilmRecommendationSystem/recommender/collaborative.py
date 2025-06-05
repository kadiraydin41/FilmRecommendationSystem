# collaborative.py
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

# Kullanıcı-Film puan matrisi
final_dataset = ratings.pivot(index='movieId', columns='userId', values='rating')
no_user_voted = ratings.groupby("movieId")['rating'].agg('count')
no_movies_voted = ratings.groupby("userId")['rating'].agg('count')

# Gürültü filtreleme
final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]
final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]

# Boşluk doldurma ve CSR matrisi
final_dataset.fillna(0, inplace=True)
csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

# Modeli eğit
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=11, n_jobs=-1)
knn.fit(csr_data)

def recommend(movie_title):
    movie = movies[movies['title'].str.contains(movie_title, case=False)]
    if not len(movie):
        return [("Movie not found", 0)]
    movie_id = movie.iloc[0]['movieId']
    if movie_id not in final_dataset['movieId'].values:
        return [("Movie not found", 0)]

    index = final_dataset[final_dataset['movieId'] == movie_id].index[0]
    distances, indices = knn.kneighbors(csr_data[index], n_neighbors=11)

    results = []
    max_dist = distances[0][1]  # ilk önerinin uzaklığı
    for i in range(1, len(distances[0])):
        movie_id = final_dataset.iloc[indices[0][i]]['movieId']
        title = movies[movies['movieId'] == movie_id]['title'].values[0]
        sim = round((1 - distances[0][i]) / (1 - max_dist) * 100, 1)
        results.append((title, sim))

    return results
