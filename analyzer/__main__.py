import json
import sys
import time
from collections import Counter
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from konlpy.tag import Okt


def language_processing(path: str, dummy_words: List[str] = None):
    print(" - Extracting")
    kt = Okt(max_heap_size=1024 * 4)

    adjectives: list = []
    nouns: list = []

    with open(path, "r", encoding="utf8") as f:
        for line in f.readlines():
            print(".", end="")
            sys.stdout.flush()
            time.sleep(0.01)
            for token in kt.pos(line, norm=True, stem=True):
                part = token[-1]
                if part == "Adjective":
                    adjectives.append(token[0])
                elif part == "Noun":
                    nouns.append(token[0])

    count = dict(Counter(adjectives).most_common())

    if not dummy_words:
        dummy_words = []

    for dummy in dummy_words:
        try:
            del count[dummy]
        except KeyError:
            continue

    with open("data/adjectives.json", "w", encoding="utf8") as data:
        data.write(json.dumps(count, ensure_ascii=False))

    with open("data/nouns.json", "w", encoding="utf8") as data:
        data.write(json.dumps(dict(Counter(nouns).most_common()), ensure_ascii=False))

    del kt


def sentimental_analyzer(
    neg_word_list: List[str], pos_word_list: List[str], path: str,
):
    print(" - Calculating...")
    kt = Okt(max_heap_size=1024 * 4)
    score_array: List[int] = []
    with open(path, encoding="utf8") as f:
        for line in f.readlines():
            time.sleep(0.05)
            if not line:
                continue
            score = 0
            line_len = len(line.split())
            for index, token in enumerate(kt.pos(line, norm=True, stem=True)):
                if token[-1] != "Adjective":
                    continue

                if token[0] in pos_word_list:
                    score += index / line_len
                elif token[0] in neg_word_list:
                    # 가설에 따른 사전선정축제 자료조사에서 만족도 중앙값에 위치한 축제 분석 시
                    # 부정적 단어가 긍정적 단어 빈도의 약 10e-2배였으므로 한번에 10씩 더 차감
                    score -= (index / line_len) + 10
            score_array.append(score)

    score = np.array(score_array)

    mu = np.mean(score)
    sigma = np.std(score)

    print("  max", np.max(score))
    print("  min", np.min(score))
    print("  ave", mu)
    print("  std", sigma)

    # 확률밀도함수 그리기
    x = np.linspace(-10, 10, 1000)
    y = (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(
        -((x - mu) ** 2) / (2 * sigma ** 2)
    )
    plt.plot(x, y, alpha=0.7, label="PDF")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(loc="upper left")
    plt.savefig("data/normal_distribution.png")
    plt.close()

    # 표준정규분표로 표준화
    i: np.ndarray = (y - mu) / sigma
    j = np.linspace(-10, 10, i.shape[0])
    plt.plot(j, i, alpha=0.7, label="SND")
    plt.xlabel("z")
    plt.ylabel("f(z)")
    plt.legend(loc="upper left")
    plt.savefig("data/standard_normal_distribution.png")
    plt.close()

    with open("data/statistics.json", "w", encoding="utf8") as f:
        f.write(
            json.dumps(
                {
                    "최대": np.max(score),
                    "최소": np.min(score),
                    "평균": mu,
                    "표준편차": sigma,
                    "array": score.tolist(),
                },
                ensure_ascii=False,
            )
        )

    del kt
