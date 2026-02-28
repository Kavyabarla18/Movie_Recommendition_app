# recommend.py
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
    df = joblib.load(pkl_path)
    print("✅ df_cleaned.pkl loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ ERROR: {e}")
    print("📋 Files in src/ folder:", os.listdir(current_dir))
    raise e


def recommend_movies(movie_name, top_n=5):
    logging.info("🎬 Recommending movies for: '%s'", movie_name)
    idx = df[df['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        logging.warning("⚠️ Movie not found in dataset.")
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    logging.info("✅ Top %d recommendations ready.", top_n)
    # Create DataFrame with clean serial numbers starting from 1
    result_df = df[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1 instead of 0
    result_df.index.name = "S.No."

    return result_df

