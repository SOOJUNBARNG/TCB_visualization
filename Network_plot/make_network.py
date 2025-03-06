# https://zenn.dev/robes/articles/a3e1a6e80efd99

from pyvis.network import Network
import pandas as pd

import pandas as pd

df = pd.read_csv("result_for_couple/word_couple_chunk_final.csv")
exclude_tokens = ['""""', "*", "1"]
df = df[~df["Token"].isin(exclude_tokens)]
df = df[~((df["Emotion_mean"] < 0.5) | (df["Emotion_count"] <= 10))]
df = df.sort_values(by="Emotion_count", ascending=False)
# Token,Verb,Emotion_mean,Emotion_count


def kyoki_word_network(df):

    got_net = Network(
        height="1000px",
        width="95%",
        bgcolor="#FFFFFF",
        font_color="black",
        notebook=True,
    )

    got_net.force_atlas_2based()
    got_data = df[:100]

    sources = got_data["Token"]
    targets = got_data["Verb"]
    weights = got_data["Emotion_count"] * got_data["Emotion_mean"]

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    for node in got_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    got_net.show_buttons(filter_=["physics"])
    return got_net


got_net = kyoki_word_network(df)
got_net.show("kyoki.html")
