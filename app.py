import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import h5py

df = pd.read_csv("data.csv")
with h5py.File("lyrics_similarity_matrix.h5", "r") as hf:
    loaded_matrix = hf["similarity_matrix"][:]
    lyrics_df = pd.DataFrame(loaded_matrix)

lyrics_similarity_matrix = cosine_similarity(lyrics_df)

def recommend_by_id(song_id, num_of_songs=10):
    idx = df.index[df["id"] == song_id].tolist()[0]
    sim_scores = list(enumerate(lyrics_similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : num_of_songs + 1]
    song_indices = [i[0] for i in sim_scores]
    return df[["id", "name"]].iloc[song_indices]


# Main function
def main():
    # Set title of the app

    st.title("Song Recommender")

    song_list = df["name"].tolist()
    # st.write("## Select a song to get recommendations:")
    selected_song = st.selectbox("Select a song to get recommendations:", song_list)
    if selected_song:
        song_id = df[df["name"] == selected_song]["id"].values[0]
        iframe = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{song_id}?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        st.markdown(iframe, unsafe_allow_html=True)

    if st.button("Recommend"):
        song_id = df[df["name"] == selected_song]["id"].values[0]
        recommendations = recommend_by_id(song_id, 5)

        st.write("## Recommended Songs:")
        for i, row in recommendations.iterrows():
            id = row["id"]
            iframe = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{id}?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
            st.markdown(iframe, unsafe_allow_html=True)


# Run the main function
if __name__ == "__main__":
    main()
