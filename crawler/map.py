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
    '''fac_num: Dict[str, int] = dict()
    for fk in facility_keywords:
        data = _automated_web(lat, long, facility_keywords[fk])
        fac_num[fk] = len(data)

    print(fac_num)

    with open("data/facilities.json", "w", encoding="utf8") as f:
        f.write(json.dumps(fac_num, ensure_ascii=False))'''
    count = 0
    for sigungu in pd.read_csv("crawler/bak.csv", encoding="cp949")['시군구명']:
        if sigungu == loc_name:
            count += 1
    with open("data/facilities.json", "w", encoding="utf8") as f:
        f.write(json.dumps({"숙박시설": count}, ensure_ascii=False))
