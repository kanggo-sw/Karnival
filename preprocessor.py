"""
산천어 송어
마임
힌우
막국수 닭갈비
"""
import json
import os
import time
from glob import glob

from analyzer.__main__ import language_processing, sentimental_analyzer
from crawler.__main__ import crawling
from crawler.map import crawling_map

_dummy_word_list = [
    # '있다' 와 같이 문장 성분 판별이 무의미한 경우 제거
    "이다",
    "있다",
    "없다",
    "아니다",
    "그렇다",
    "스럽다",
    "이렇다",
    # 감정을 드러내지 않는 형용사 제거
    "어떻다",
    "많다",
    "적다",
    "크다",
    "작다",
    "필요하다",
    "두껍다",
    "얇다",
    "유리하다",
    "당연하다",
    "가능하다",
    "같다",
]
_pos_word_list = [
    "좋다",
    "예쁘다",
    "재미있다",
    "즐겁다",
    "화려하다",
    "만족스럽다",
    "맛있다",
    "아름답다",
    "재밌다",
    "신나다",
    "알차다",
    "시원하다",
    "근사하다",
    "친절하다",
    "영롱하다",
    "편안하다",
    "멋지다",
    "행복하다",
]
_neg_word_list = [
    "아쉽다",
    "춥다",
    "비싸다",
    "밉다",
    "딱하다",
    "어렵다",
    "싫다",
    "싫어하다",
    "차갑다",
    "힘들다",
    "시리다",
    "아프다",
    "아찔하다",
    "해롭다",
    "뒤늦다",
    "어이없다",
    "실망하다",
    "썰렁하다",
    "기괴하다",
    "싸하다",
    "따갑다",
    "위험하다",
    "심드렁하다",
    "불편하다",
    "민망하다",
    "지겹다",
    "재미없다",
    "좁다",
    "단순하다",
    "부족하다",
    "안좋다",
    "배고프다",
]

start_time = time.time()

# Parameters
taekwanryeong = {
    # 축제명
    "name": "대관령 눈꽃축제",
    # 검색 키워드
    "keywords": ["2019 대관령 눈꽃축제 후기"],
    # 검색 엔진
    "engines": ["NAVER"],
    # 분석에 유용하지 않은 어휘들
    "dummy_word_list": _dummy_word_list,
    # 긍정 어휘
    "pos_word_list": _pos_word_list,
    # 부정 어휘
    "neg_word_list": _neg_word_list,
    # 축제 지역 위도
    "lat": 37.370474,
    # 축제 지역 경도
    "long": 128.3899769,
    # 시설 분류별 구글 지도 검색 키워드
    "facility_keywords": {"숙박시설": ["강원도 평창군 대관령면 숙박시설"], "음식점": ["강원도 평창군 대관령면 음식점"]},
    "local_name": "평창군"
}

taebaek = {
    # 축제명
    "name": "태백산 눈축제",
    # 검색 키워드
    "keywords": ["2019 태백산 눈축제 후기"],
    # 검색 엔진
    "engines": ["NAVER"],
    # 분석에 유용하지 않은 어휘들
    "dummy_word_list": _dummy_word_list,
    # 긍정 어휘
    "pos_word_list": _pos_word_list,
    # 부정 어휘
    "neg_word_list": _neg_word_list,
    # 축제 지역 위도
    "lat": 37.1640654,
    # 축제 지역 경도
    "long": 128.9855649,
    # 시설 분류별 구글 지도 검색 키워드
    "facility_keywords": {"숙박시설": ["강원도 태백시 숙박시설"], "음식점": ["강원도 태백시 음식점"]},
    "local_name": "태백시"
}

hwacheon = {
    # 축제명
    "name": "화천 실내얼음조각광장",
    # 검색 키워드
    "keywords": ["실내얼음조각광장 후기"],
    # 검색 엔진
    "engines": ["NAVER"],
    # 분석에 유용하지 않은 어휘들
    "dummy_word_list": _dummy_word_list,
    # 긍정 어휘
    "pos_word_list": _pos_word_list,
    # 부정 어휘
    "neg_word_list": _neg_word_list,
    "lat": 38.14212,
    "long": 127.67615,
    # 시설 분류별 구글 지도 검색 키워드
    "facility_keywords": {"숙박시설": ["강원도 화천군 숙박시설"], "음식점": ["강원도 화천군 음식점"]},
    "local_name": "화천군"
}

jsons = []

for json_file in glob("./*.json"):
    json_dict = json.loads(open(json_file, encoding="utf8").read())
    json_dict["dummy_word_list"] = _dummy_word_list
    json_dict["neg_word_list"] = _neg_word_list
    json_dict["pos_word_list"] = _pos_word_list
    jsons.append(json_dict)

print("예상완료시간: 약 {}분 이상".format(len(jsons) * 70. / 60.))

for target_parameters in jsons:
    if os.path.isdir(target_parameters["name"]):
        print("[!] " + target_parameters["name"] + " is already processed. continue...")
        continue
    print("[+] Step 1. Crawling data")
    crawling(
        keywords=target_parameters["keywords"],
        engines=target_parameters["engines"],
        output=target_parameters["name"],
    )
    print("Done.\n")

    print("[+] Step 2. Extract the original form of the adjectives from data")
    language_processing(
        "data/raw/{}.txt".format(target_parameters["name"]),
        dummy_words=target_parameters["dummy_word_list"],
    )
    print("Done.\n")

    print("[+] Step 3. Sentimental analyzer")
    sentimental_analyzer(
        neg_word_list=target_parameters["neg_word_list"],
        pos_word_list=target_parameters["pos_word_list"],
        path="data/raw/{}.txt".format(target_parameters["name"]),
    )
    print("Done.\n")

    print("[+] Step 4. Crawling map data")
    crawling_map(
        target_parameters["facility_keywords"],
        target_parameters["lat"],
        target_parameters["long"],
        loc_name=target_parameters['local_name']
    )
    print("Done.\n")

    print("[+] Step 5. Save parameters")
    with open("data/param.json", "w", encoding="utf8") as f:
        f.write(json.dumps(target_parameters, ensure_ascii=False))
    print("Done.\n")

    print("[+] Final. Rename directory")
    os.rename("data", target_parameters["name"])
    print("Done.\n")

print(f"Process completed in {time.time() - start_time}s.")
