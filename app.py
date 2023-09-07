import streamlit as st
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://spotify:hDvSHlgkbAldOsWS@spotify.yjp9nvd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))

db = client["spofity_features"]
features = db["features"]
similarity = db["similarity"]

df = pd.read_csv("data.csv")


def get_recommendations(song_id, num_of_songs=10):
    target_record = features.find_one({"id": song_id})

    if target_record and "cosine" in target_record:
        target_cosine = np.array(target_record["cosine"])

    sorted_indices = np.argsort(target_cosine)[::-1][1 : num_of_songs + 1]

    similar_record = []

    for idx in sorted_indices:
        similar_record.append(
            features.find_one({"df_idx": int(idx)}, {"_id": 0, "id": 1, "name": 1})
        )

    return similar_record


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
        recommendations = get_recommendations(song_id, 5)

        st.write("## Recommended Songs:")
        for row in recommendations:
            id = row["id"]
            iframe = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{id}?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
            st.markdown(iframe, unsafe_allow_html=True)


# Run the main function
if __name__ == "__main__":
    main()
