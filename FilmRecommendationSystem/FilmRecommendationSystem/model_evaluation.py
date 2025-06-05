import time
from recommender.content_based import recommend as cb_recommend
from recommender.collaborative import recommend as cf_recommend
from recommender.hybrid import hybrid_recommend

def benchmark_models(movie_name="Avatar"):
    results = []
    # Content-Based
    start = time.time()
    cb = cb_recommend(movie_name)
    t_cb = round((time.time() - start) * 1000, 2)
    avg_cb = round(sum([sim for _, sim in cb]) / len(cb), 2)
    # Collaborative
    start = time.time()
    cf = cf_recommend(movie_name)
    t_cf = round((time.time() - start) * 1000, 2)
    avg_cf = round(sum([sim for _, sim in cf]) / len(cf), 2)
    # Hybrid
    start = time.time()
    hybrid = hybrid_recommend(movie_name)
    t_hybrid = round((time.time() - start) * 1000, 2)
    avg_hybrid = round(sum([sim for _, sim in hybrid]) / len(hybrid), 2)
    return {
        "models": ["Content-Based", "Collaborative", "Hybrid"],
        "times": [t_cb, t_cf, t_hybrid],
        "similarities": [avg_cb, avg_cf, avg_hybrid]
    }
