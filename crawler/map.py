import json
import time
from typing import List, Dict

from selenium import webdriver
import pandas as pd

def _automated_web(lat: float, long: float, keywords: List[str]) -> List[str]:
    driver = webdriver.Chrome("./chromedriver")
    facilities: List[str] = []

    for keyword in keywords:
        # 구글 지도 접속
        driver.get(
            "https://www.google.co.kr/maps/@{lat},{long},16z?hl=ko".format(
                lat=lat, long=long
            )
        )
        driver.find_element_by_css_selector("input#searchboxinput").send_keys(keyword)

        # 검색버튼 누르기
        driver.find_element_by_css_selector("button#searchbox-searchbutton").click()

        while True:
            time.sleep(5)

            # 컨테이너(가게) 데이터 수집 // div.section-result-content
            stores = driver.find_elements_by_css_selector("div.section-result-content")
            for s in stores:
                title = s.find_element_by_css_selector("h3.section-result-title").text
                facilities.append(title)
            # noinspection PyBroadException
            try:
                driver.find_element_by_css_selector(
                    "button#n7lv7yjyC35__section-pagination-button-next"
                ).click()
            except Exception:
                # 다음 버튼이 없으면 종료
                break

    driver.close()

    # 중복 제거해서 반환
    return list(set(facilities))


def crawling_map(facility_keywords: Dict[str, List[str]], lat, long, loc_name:str=None):
    c1 = 0
    for sigungu in pd.read_csv("crawler/전국민박펜션업소표준데이터.csv", encoding="cp949", low_memory=False)['소재지도로명주소']:
        if not isinstance(sigungu, str):
            continue
        if loc_name in sigungu:
            c1 += 1

    c2 = 0
    for sigungu in pd.read_csv("crawler/전국전기차충전소표준데이터.csv", encoding="cp949", low_memory=False)['소재지도로명주소']:
        if not isinstance(sigungu, str):
            continue
        if loc_name in sigungu:
            c2 += 1

    c3 = 0
    for sigungu in pd.read_csv("crawler/전국관광안내소표준데이터.csv", encoding="cp949", low_memory=False)['소재지도로명주소']:
        if not isinstance(sigungu, str):
            continue
        if loc_name in sigungu:
            c3 += 1

    c4 = 0
    for sigungu in pd.read_csv("crawler/전국금연구역표준데이터.csv", encoding="cp949", low_memory=False)['소재지도로명주소']:
        if not isinstance(sigungu, str):
            continue
        if loc_name in sigungu:
            c4 += 1

    fac_num: Dict[str, int] = dict()
    for fk in facility_keywords:
        data = _automated_web(lat, long, facility_keywords[fk])
        fac_num[fk] = len(data)

    fac_num["숙박시설"] = c1
    fac_num["전기차충전소"] = c2
    fac_num["관광안내소"] = c3
    fac_num["금연구역"] = c4

    print(loc_name, fac_num)

    with open("data/facilities.json", "w", encoding="utf8") as f:
        f.write(json.dumps(fac_num, ensure_ascii=False))
