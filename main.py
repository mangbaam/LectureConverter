import json

path = "C:/Users/audqj/OneDrive - suwon.ac.kr/자료/classmate/강의목록/realtimeDB.json"
lecturePath = "C:/Users/audqj/OneDrive - suwon.ac.kr/자료/classmate/강의목록/USW_2021_2.json"
translate = {
    "subjtCd": "과목 코드",
    "subjtNm": "과목명",
    "timtSmryCn": "시간표",
    "ltrPrfsNm": "교수자",
    "estbDpmjNm": "개설 부서",
    "point": "학점",
    "facDvnm": "이수구분",
    "trgtGrdeCd": "개설 학년",
    "cltTerrCd": "교양 영역",
}
cltTerr = {
    "41": "1영역-언어와 소통",
    "42": "2영역-세계와 문명",
    "43": "3영역-역사와 사회",
    "44": "4영역-문화와 철학",
    "45": "5영역-기술과 정보",
    "46": "6영역-건강과 예술",
    "47": "7영역-자연과 과학"
}


def addLecture(school, term):
    f = open(lecturePath, encoding='utf-8')
    lectures = json.load(f)
    f.close()
    lectureList = dict()
    for lecture in lectures:
        # 폐강 과목 제외
        if "closeDt" in lecture.keys() or "closeResnCn" in lecture.keys():
            continue
        # 키: 과목코드-분반
        key = lecture["subjtCd"] + '-' + lecture["diclNo"]
        # 과목 정보 저장
        infos = dict()
        for column in lecture.keys():
            if column in translate.keys():
                # 교양 영역 처리
                if column == "cltTerrCd":
                    infos[translate[column]] = cltTerr[lecture[column]]
                # 시간, 장소정보 분리
                elif column == "timtSmryCn":
                    timeSummary = lecture[column].split('),')
                    print(timeSummary)
                    timeAndPlaces = []
                    for info in timeSummary:
                        print(info, end=' ')
                        time, place = info.rstrip(')').split('(')
                        tpData = {"time": time, "place": place}
                        timeAndPlaces.append(tpData)
                    print()
                    infos["시간 및 장소"] = timeAndPlaces

                else:
                    infos[translate[column]] = lecture[column]
        lectureList[key] = infos
    print(lectureList.items())

    f = open(path, encoding='utf-8')
    realtimeDB = json.load(f)
    f.close()

    if school not in realtimeDB.keys():
        raise Exception("사용 불가한 학교입니다.")
    elif term not in realtimeDB[school].keys():
        raise Exception("해당 학기 정보가 없습니다.")
    else:
        realtimeDB[school][term] = lectureList

    # 기존의 DB 대체
    outfile = open(path, 'w', encoding='utf-8')
    json.dump(realtimeDB, outfile)
    outfile.close()


def change():
    f = open(path, encoding='utf-8')
    data = json.load(f)
    lectures = data['USW']
    new_data = {'USW': {'Lectures': {'2021_2': lectures}}}

    outfile = open(path, 'w', encoding='utf-8')
    json.dump(new_data, outfile)

    outfile.close()
    f.close()


if __name__ == '__main__':
    # addLecture("USW", "2021_2")
    change()
