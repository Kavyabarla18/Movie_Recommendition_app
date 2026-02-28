import joblib
import logging
import streamlit as st
import os

# Setup logging (keep your original)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🔁 Loading data...")
current_dir = os.path.dirname(os.path.abspath(__file__))
pkl_path = os.path.join(current_dir, 'df_cleaned.pkl')

try:
    df = joblib.load("src/df_cleaned.pkl")
    cosine_sim = joblib.load("src/similarity.pkl")  # ADD THIS LINE
except FileNotFoundError as e:
    st.error(f"❌ Missing file: {e}")
    st.stop()

def recommend_movies(title):
    # Safe movie lookup
    movie_matches = df[df['title'].str.contains(title, case=False, na=False)]
    if movie_matches.empty:
        return ["Movie not found - try exact title"]
    
    idx = movie_matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))  # Now cosine_sim exists!
    movie_indices = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    
    recommended_movies = []
    for i in movie_indices:
        recommended_movies.append(df.iloc[i[0]]['title'])
    
    return recommended_movies


