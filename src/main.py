import streamlit as st
import json
import pandas as pd

# FIRST: set_page_config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Safe data loading
@st.cache_data
def load_data():
    try:
        from recommend import df, recommend_movies
        return df, recommend_movies
    except:
        return pd.DataFrame(), lambda x: []

df, recommend_movies = load_data()

st.title("🎬 Movie Recommendation System")
st.markdown("---")

if df.empty:
    st.error("❌ No data loaded. Check src/recommend.py")
    st.stop()

# Debug: Show actual columns
st.sidebar.header("📊 Dataset Info")
st.sidebar.write(f"**Shape:** {df.shape}")
st.sidebar.write(f"**Columns:** {list(df.columns)}")

# Safe column access
title_col = 'title' if 'title' in df.columns else df.columns[0]
st.sidebar.metric("Total Movies", len(df))

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Select Movie")
    movies_list = df[title_col].drop_duplicates().tolist()
    selected_movie = st.selectbox(
        "Choose a movie:",
        options=movies_list[:1000] if movies_list else ["No data"],
        index=0
    )

with col2:
    st.header("ℹ️ Movie Info")
    movie_row = df[df[title_col] == selected_movie]
    if not movie_row.empty:
        movie_info = movie_row.iloc[0]
        # Safe metrics - use first available numeric column
        for col in df.select_dtypes(include=['number']).columns[:2]:
            st.metric(col.capitalize(), movie_info.get(col, 0))

# Recommendations
if st.button("🚀 Get Recommendations", type="primary"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        
        if not recommendations or recommendations[0].startswith("❌"):
            st.warning(recommendations[0])
        else:
            st.success(f"🎬 Top movies like '{selected_movie}':")
            for i, movie in enumerate(recommendations, 1):
                st.write(f"{i}. **{movie}**")

# FIXED Preview - Safe columns only
with st.expander("📋 Preview Dataset"):
    available_cols = [col for col in ['title', 'genres', 'vote_average'] if col in df.columns]
    if available_cols:
        st.dataframe(df[available_cols].head())
    else:
        st.dataframe(df.head())

