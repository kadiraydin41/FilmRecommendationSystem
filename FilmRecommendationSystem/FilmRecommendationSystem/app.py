from flask import Flask, render_template, request, jsonify, redirect, session
from recommender.hybrid import hybrid_recommend
from recommender.content_based import recommend as cb_recommend
from recommender.collaborative import recommend as cf_recommend
from recommender.tmdb import get_movie_info
from recommender.db import clear_favorites, add_favorite, get_favorites, save_history
from model_evaluation import benchmark_models
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = "super_secret_key"

movie_df = pd.read_csv("data/tmdb_5000_movies.csv")
movie_titles = movie_df['title'].dropna().unique().tolist()

def normalize_title(title):
    """
    Film başlığını normalize eder:
    - Parantez içi ifadeleri kaldırır
    - Baş ve sondaki boşlukları siler
    - Küçük harfe çevirir
    """
    if not isinstance(title, str):
        return ""
    title = re.sub(r"\([^)]*\)", "", title)
    return title.strip().lower()

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")



@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect("/login")
    movie_name = request.values.get("movie", "")
    selected_filter = request.values.get("filter", "hybrid")
    movie_infos = []
    if movie_name:
        if selected_filter == "cb":
            recommendations = cb_recommend(movie_name)
        elif selected_filter == "cf":
            recommendations = cf_recommend(movie_name)
        else:
            recommendations = hybrid_recommend(movie_name)
        username = session.get("username", "anon")
        fav_titles_raw = [title for title, _ in get_favorites(username)]
        fav_titles_normalized = [normalize_title(t) for t in fav_titles_raw]
        for title, sim in recommendations:
            info = get_movie_info(title)
            if info:
                info["similarity"] = sim
                info["is_favorite"] = normalize_title(title) in fav_titles_normalized
                movie_infos.append(info)
        if request.method == "POST":
            save_history(username, movie_name, [title for title, _ in recommendations])
    return render_template("index.html", recommendations=movie_infos,
                           movie=movie_name, selected_filter=selected_filter)



# Autocomplete route
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("q", "").lower()
    matches = [title for title in movie_titles if query in title.lower()]
    return jsonify(matches[:10])

# Model karşılaştırma sayfası
@app.route("/compare")
def compare_models():
    data = benchmark_models("Avatar")
    return render_template("compare.html", models=data["models"],
                           times=data["times"], similarities=data["similarities"])



# Giriş sayfası
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return redirect("/")
    return render_template("login.html")

from recommender.db import get_favorites

from recommender.db import remove_favorite  # yukarıya ekle

# Favoriye ekleme
@app.route("/favorite", methods=["POST"])
def favorite():
    title = request.form["title"]
    movie = request.form.get("movie", "")
    selected_filter = request.form.get("filter", "hybrid")
    username = session.get("username", "anon")
    add_favorite(username, title)
    return redirect(f"/?movie={movie}&filter={selected_filter}")

@app.route("/favorites")
def show_favorites():
    username = session.get("username", "anon")
    favorites = get_favorites(username)
    movie_infos = []
    for title, _ in favorites:
        info = get_movie_info(title)
        if info:
            movie_infos.append(info)
    return render_template("favorites.html", recommendations=movie_infos)


@app.route("/clear_favorites")
def clear_all_favorites():
    username = session.get("username", "anon")
    clear_favorites(username)
    return "Tüm favoriler silindi!"



@app.route("/unfavorite", methods=["POST"])
def unfavorite():
    title = request.form["title"]
    movie = request.form.get("movie", "")
    selected_filter = request.form.get("filter", "hybrid")
    username = session.get("username", "anon")
    remove_favorite(username, title)
    if movie:
        return redirect(f"/?movie={movie}&filter={selected_filter}")
    else:
        return redirect("/favorites")




if __name__ == "__main__":
    app.run(debug=True)