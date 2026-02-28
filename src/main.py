# app.py
import json
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details


current_dir = os.path.dirname(os.path.abspath(__file__))  # /mount/src/movie_recommendition_app/src/
config_path = os.path.join(current_dir, "config.json")

print(f"🔍 Looking for config: {config_path}")
print(f"📁 src/ contents: {os.listdir(current_dir)}")

try:
    config = json.load(open(config_path))
    print("✅ config.json loaded!")
except FileNotFoundError as e:
    print(f"❌ config.json missing!")
    raise e


# OMDB api key
OMDB_API_KEY = config["OMDB_API_KEY"]

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommender")

# Using 'title' instead of 'song' now
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=100)
                        else:
                            st.write("❌ No Poster Found")
                    with col2:
                        st.markdown(f"### {movie_title}")
                        st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")
