import streamlit as st
from recommend import df, recommend_movies
import json

# ✅ LINE 2: FIRST Streamlit command (NO imports/calls before this!)
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Load config AFTER set_page_config
try:
    with open("src/config.json", 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"top_n": 10}

st.title("🎬 Movie Recommendation System")
st.markdown("---")

# Sidebar
st.sidebar.header("📊 Dataset Info")
st.sidebar.metric("Total Movies", len(df))
st.sidebar.metric("Features", df.shape[1])

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Select Movie")
    movies_list = df['title'].drop_duplicates().tolist()
    selected_movie = st.selectbox(
        "Choose a movie:",
        options=movies_list[:1000],
        index=0
    )

with col2:
    st.header("ℹ️ Movie Info")
    if selected_movie in df['title'].values:
        movie_info = df[df['title'] == selected_movie].iloc[0]
        st.metric("Year", movie_info.get('year', 'N/A'))
        st.metric("Vote Average", f"{movie_info.get('vote_average', 0):.1f}/10")

# Recommendations button
if st.button("🚀 Get Recommendations", type="primary"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        
        if not recommendations or recommendations[0].startswith("❌"):
            st.warning(recommendations[0])
        else:
            st.success(f"🎬 Top movies like '{selected_movie}':")
            for i, movie in enumerate(recommendations, 1):
                st.write(f"{i}. **{movie}**")

with st.expander("📋 Preview Dataset"):
    st.dataframe(df[['title', 'genres', 'vote_average']].head())
