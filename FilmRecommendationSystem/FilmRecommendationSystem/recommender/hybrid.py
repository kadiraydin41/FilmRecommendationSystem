# hybrid.py
from recommender.content_based import recommend as cb_recommend
from recommender.collaborative import recommend as cf_recommend

def hybrid_recommend(movie_title, weight_cb=0.5, weight_cf=0.5):
    cb_results = cb_recommend(movie_title)
    cf_results = cf_recommend(movie_title)
    if cb_results == [("Movie not found", 0)] and cf_results == [("Movie not found", 0)]:
        return []
    scores = {}
    for title, score in cb_results:
        scores[title] = scores.get(title, 0) + score * weight_cb
    for title, score in cf_results:
        scores[title] = scores.get(title, 0) + score * weight_cf
    max_score = max(scores.values()) if scores else 1
    final = [(title, round((score / max_score) * 100, 1)) for title, score in scores.items()]
    sorted_final = sorted(final, key=lambda x: x[1], reverse=True)
    return sorted_final[:10]





