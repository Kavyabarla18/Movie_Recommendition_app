import joblib
import streamlit as st
import pandas as pd
import numpy as np
import os
import logging

# Remove problematic logging/file writes for Streamlit Cloud
st.info("🔁 Loading data...")

# BULLETPROOF path for Streamlit Cloud
try:
    df = joblib.load("src/df_cleaned.pkl")
    st.success("✅ Data loaded!")
except FileNotFoundError:
    st.error("❌ Missing src/df_cleaned.pkl - upload to GitHub!")
    st.stop()

# Load or compute cosine similarity matrix
try:
    cosine_sim = joblib.load("src/similarity.pkl")
except FileNotFoundError:
    st.warning("⚠️ Computing similarity matrix...")
    # Compute TF-IDF or whatever features you used
    tfidf_matrix = df['overview'].fillna('')  # Adjust based on your features
    cosine_sim = cosine_similarity(tfidf_matrix)
    joblib.dump(cosine_sim, "src/similarity.pkl")

def recommend_movies(title):
    """Safe movie recommendation with error handling"""
    try:
        # Safe movie lookup with fuzzy matching
        movie_matches = df[df['title'].str.contains(title, case=False, na=False)]
        if movie_matches.empty:
            return ["❌ Movie not found. Try 'Inception', 'Titanic', 'Avatar'"]
        
        idx = movie_matches.index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        movie_indices = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
        
        # Get recommended movie titles
        recommended_movies = []
        for i in movie_indices:
            recommended_movies.append(df.iloc[i[0]]['title'])
        
        return recommended_movies
        
    except Exception as e:
        return [f"❌ Error: {str(e)}"]

# Make functions globally available
df = df  # Global DataFrame
recommend_movies = recommend_movies  # Global function
