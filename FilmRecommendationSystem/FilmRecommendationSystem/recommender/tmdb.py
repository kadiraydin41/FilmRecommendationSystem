import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAIL_URL = "https://api.themoviedb.org/3/movie/{}"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def get_movie_info(title):
    params = {"api_key": API_KEY, "query": title}
    r = requests.get(TMDB_SEARCH_URL, params=params)
    results = r.json().get("results")
    if not results:
        return None
    movie = results[0]
    movie_id = movie["id"]
    detail_url = TMDB_DETAIL_URL.format(movie_id)
    r = requests.get(detail_url, params={"api_key": API_KEY})
    data = r.json()
    return {
        "title": data.get("title"),
        "overview": data.get("overview"),
        "genres": ", ".join([g["name"] for g in data.get("genres", [])]),
        "runtime": f"{data.get('runtime', 0)} dk",
        "poster": IMAGE_BASE + data["poster_path"] if data.get("poster_path") else None,
        "rating": round(data.get("vote_average", 0), 1)  # ⭐ buraya dikkat
    }


