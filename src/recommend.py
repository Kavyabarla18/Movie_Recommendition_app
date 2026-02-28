import joblib
import logging
import streamlit as st
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🔁 Loading data...")
current_dir = os.path.dirname(os.path.abspath(__file__))  # /mount/src/movie_recommendition_app/src/
pkl_path = os.path.join(current_dir, 'df_cleaned.pkl')

print(f"🔍 Looking for: {pkl_path}")  # Debug
print(f"📁 Current dir contents: {os.listdir(current_dir)}")  # Shows if file exists

try:
    df = joblib.load("src/df_cleaned.pkl")
except FileNotFoundError:
    st.error("❌ Missing src/df_cleaned.pkl - upload to GitHub!")
    st.stop()


def recommend_movies(title):
    # Safe movie lookup
    movie_matches = df[df['title'].str.contains(title, case=False, na=False)]
    
    # FIX: Check if matches exist BEFORE indexing
    if movie_matches.empty:
        return ["Movie not found - try exact title from dropdown"]
    
    idx = movie_matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    movie_indices = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    
    recommended_movies = []
    for i in movie_indices:
        recommended_movies.append(df.iloc[i[0]]['title'])
    
    return recommended_movies

