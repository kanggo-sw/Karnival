import itertools
import json

import altair as alt
import folium
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Parameters

festivals = ["태백산 눈축제", "대관령 눈꽃축제", "화천 실내얼음조각광장"]
facility_to_viz = "숙박시설"
m = folium.Map(
    [(38.642618 + 37.018205) / 2, (127.080231 + 129.371910) / 2],
    zoom_start=8,
)

_satisfaction_indexed = []
scaled_satisfaction = {}
_facilities_indexed = []
scaled_facilities = {}

statistics_scalar = MinMaxScaler()
facilities_scalar = MinMaxScaler()

for i, festival in enumerate(festivals):
    statistics = json.loads(open(f"{festival}/statistics.json", encoding="utf8").read())
    facilities = json.loads(open(f"{festival}/facilities.json", encoding="utf8").read())

    _satisfaction_indexed.append([statistics["평균"]])
    _facilities_indexed.append([facilities[facility_to_viz]])

statistics_scalar.fit(_satisfaction_indexed)
_satisfaction_indexed = statistics_scalar.transform(_satisfaction_indexed)
for i, festival in enumerate(festivals):
    scaled_satisfaction[festival] = _satisfaction_indexed[i][0]

_facilities_indexed_original = _facilities_indexed.copy()
facilities_scalar.fit(_facilities_indexed)
_facilities_indexed = facilities_scalar.transform(_facilities_indexed)
for i, festival in enumerate(festivals):
    scaled_facilities[festival] = _facilities_indexed[i][0]

for i, festival in enumerate(festivals):
    param = json.loads(open(f"{festival}/param.json", encoding="utf8").read())

    _adj_json = json.loads(open(f"{festival}/adjectives.json", encoding="utf8").read())

    _adj_json = dict(itertools.islice(_adj_json.items(), 26))
    adj_data = {}
    for j, key in enumerate(_adj_json):
        adj_data[f"{chr(j + 97)}.{key}"] = _adj_json[key]

    df = pd.DataFrame(
        {"x": [key for key in adj_data], "y": [adj_data[key] for key in adj_data]}
    )

    chart = alt.Chart(df).mark_bar().encode(x="x", y="y",)
    chart = json.loads(chart.to_json())

    folium.Marker(
        location=(param["lat"], param["long"]),
        tooltip=f"{param['name']}<br />상대적 만족도:{scaled_satisfaction[festival]}",
        popup=folium.Popup().add_child(folium.VegaLite(chart)),
        icon=folium.Icon(color="black", icon_color="#FFFF00", icon="check")
        if scaled_satisfaction[festival] == np.max(_satisfaction_indexed)
        else None,
    ).add_to(m)

    folium.CircleMarker(
        location=(param["lat"], param["long"]),
        tooltip=f"인프라({_facilities_indexed_original[i][0]}개)",
        radius=(scaled_facilities[festival] + 1) * 10 - 1,
        color="#3186cc",
        fill_color="#3186cc",
    ).add_to(m)

m.save(f"{festivals[0]} 등 시각화.html")
