from mapboxgl import ChoroplethViz
from mapboxgl.utils import create_color_stops, create_numeric_stops


def show():
    # Map
    token = "pk.eyJ1IjoidGRoODMxNiIsImEiOiJja2t2MXRtcXE0ZXZiMm9sYWkyaHF3ZjY5In0.H6RzmgQm_o7a_ywM1qV2Sw"
    # 강원도 중심부의 경도, 위도 입니다.
    center = [128, 37.5]

    # 시각화 할 값에 따른 색상의 범주를 지정해줍니다.
    color_breaks = [0, 10, 20, 30, 40, 50]
    color_stops = create_color_stops(color_breaks, colors="BuPu")
    viz = ChoroplethViz(
        access_token=token,
        data=None,
        color_property="인지도",
        color_stops=color_stops,
        center=center,
        zoom=7.5,
    )
    # 맵을 -15도 만큼 좌우 회전하고, 45도 만큼 상하 회전합니다.
    viz.bearing = -15
    viz.pitch = 45

    # 높이의 값을 '인구' 에 따라 아래 간격으로 매핑합니다.
    numeric_stops = create_numeric_stops([0, 10, 20, 30, 40, 50], 0, 3000)

    viz.height_stops = numeric_stops
    viz.height_function_type = "interpolate"
    # 맵을 출력합니다.
    viz.show()
