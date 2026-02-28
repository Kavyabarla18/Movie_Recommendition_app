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
    df = joblib.load("src/df_cleaned.pkl")
except FileNotFoundError:
    st.error("❌ Missing src/df_cleaned.pkl - upload to GitHub!")
    st.stop()


def recommend_movies(title):
    # Safe movie lookup
    movie_matches = df[df['title'].str.contains(title, case=False, na=False)]
  if st.button("Get Recommendations"):
    recommendations = recommend_movies(selected_movie)
    
     if not recommendations or recommendations == ["Movie not found in database!"]:
        st.warning("❌ No recommendations. Try 'Inception', 'Titanic'")
     else:
        st.success(f"🎬 Top 10 movies like '{selected_movie}':")
         for i, movie in enumerate(recommendations, 1):
            st.write(f"{i}. {movie}")

    
    recommended_movies = []
    for i in movie_indices:
        recommended_movies.append(df.iloc[i[0]]['title'])
    
    return recommended_movies


