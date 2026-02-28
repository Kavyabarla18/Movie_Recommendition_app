import joblib
import logging
import streamlit as st
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging (keep yours)
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
except FileNotFoundError:
    st.error("❌ Missing src/df_cleaned.pkl")
    st.stop()

# AUTO-GENERATE similarity.pkl if missing
try:
    cosine_sim = joblib.load("src/similarity.pkl")
    st.success("✅ similarity.pkl loaded!")
except FileNotFoundError:
    st.info("⚙️ Generating similarity matrix...")
    
    # Create text features for cosine similarity (adjust column name)
    df['features'] = df['overview'].fillna('') + ' ' + df['genres'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf.fit_transform(df['features'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    
    # Save for next time
    joblib.dump(cosine_sim, "src/similarity.pkl")
    st.success("✅ similarity.pkl generated & saved!")

def recommend_movies(title):
    movie_matches = df[df['title'].str.contains(title, case=False, na=False)]
    if movie_matches.empty:
        return ["Movie not found - try exact title"]
    
    idx = movie_matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    movie_indices = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    
    recommended_movies = []
    for i in movie_indices:
        recommended_movies.append(df.iloc[i[0]]['title'])
    
    return recommended_movies



