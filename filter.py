from playwright.sync_api import Playwright, sync_playwright, expect
from selenium.webdriver.common.by import By
from selenium import webdriver
import sqlite3
import re
import sys
from time import localtime, strftime



time = localtime()
screenshot_time = strftime('%Y-%m-%d', time)

def fetch_urls():
    with sqlite3.connect("./illegals.db") as db_connection:
        cur = db_connection.cursor()
        cur.execute("SELECT main_url from illegal_sites where site_available IS NULL")
        row = cur.fetchall()
        url_raw = re.findall(
            'http[s]?://(?:[a-zA-Z-ㄱ-ㅣ가-힣]|[0-9]|[$\-@\.&+:/?=_&;]|[!*\(\),]|(?:%[0-9a-fA-F-ㄱ-ㅣ가-힣][0-9a-fA-F-ㄱ-ㅣ가-힣]))+',
            str(row))
        return url_raw

def fetch_expected_category(url):
    with sqlite3.connect("./illegals.db") as category_conn:
        cur = category_conn.cursor()
        sql = "SELECT " + "expected_category" + " from illegal_sites WHERE main_url = ?"
        cur.execute(sql, (url,))
        category_raw = cur.fetchone()
        category = re.sub('[-=+,‘|\(\)\'…》]','', str(category_raw))

        if category == 'adult':
            return '성인'
        elif category == 'gamble':
            return '도박'
        elif category == 'webtoon':
            return '웹툰'
        elif category == 'torrent':
            return '토렌트'
        elif category == 'prostitution':
            return '성매매'
        elif category == 'streaming':
            return '스트리밍'
        else:
            return '유해'

def reporting(url, url_go):
    print(">>> [Reporting]...")
    category = fetch_expected_category(url)
    reporting_url = "http://www.kocsc.or.kr/sec/rnc/iPinCert.do?preContent=+1.+%EB%AF%BC%EC%9B%90%EC%B7%A8%EC%A7%80+%0A-%0A2.+%EB%AF%BC%EC%9B%90%EB%82%B4%EC%9A%A9+%0A-&conText=%2Fmain&joinType=13&explain=true"

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 11; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/89.0.4389.72 Mobile Safari/537.36')
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome('D:\chromedriver.exe', options=options)
    file_path = "D:\\Crawler\\2022_Copyright_Crawler\\screenshot\\" + screenshot_time + '\\' + url_go + ".png"

    # 양식 기입
    driver.get(reporting_url)
    driver.find_element_by_css_selector("#login1").send_keys("김민지")
    driver.find_element_by_css_selector("#login2").send_keys("19961101")
    driver.find_element_by_class_name("login-type-btn").click()
    driver.find_element_by_class_name("in_box.in_length150").send_keys("taylor1101@@")
    driver.find_element_by_class_name("btn_t2").click()
    driver.find_element_by_css_selector("#password").send_keys("taylor1101@@")
    driver.find_element_by_css_selector("#password_re").send_keys("taylor1101@@")
    driver.find_element_by_css_selector("#password_ca").send_keys("blue")
    driver.find_element_by_css_selector("#mobile2").send_keys("9165")
    driver.find_element_by_css_selector("#mobile3").send_keys("0864")
    driver.find_element_by_css_selector("#email1").send_keys("johnnytaylor1101")
    driver.find_element_by_css_selector("#email2").send_keys("gmail.com")
    driver.find_element(By.XPATH, '// *[@id="female"]').click()
    driver.find_element_by_class_name("btn_t3").click()
    driver.find_element_by_css_selector("#url").send_keys(url)
    driver.find_element_by_css_selector("#subject").send_keys("[%s]유해사이트 신고합니다_" %category, url_go)
    driver.find_element_by_css_selector("#cont").send_keys("유해 " + category +"사이트 신고하오니 조치 부탁 드리겠습니다.")
    driver.find_element(By.XPATH, '//input[@id="ComFileUploader"]').send_keys(file_path)
    driver.find_element_by_css_selector("#agree").click()
    driver.find_element_by_css_selector("#board > div.js_tab_box.selected > p > a:nth-child(2)").click()

    # 알람창 처리
    alert = driver.switch_to.alert
    alert.accept()
    alert.accept()

    driver.close()


def filtering(title, body):

    light_illegal_keywords = ['애니','웹툰', '미리보기', '유료', '무료', '망가', '인기', '만화', '썰', '순위',
                              '다시보기', '드라마', '티비', '스트리밍', '링크', 'streaming', 'STREAMING', 'Streaming', 'STREAMS', 'Streams', 'stream', 'Streams', 'STREAMS',
                              '실시간', '최신', '주소', '토렌트', 'torrent', 'TORRENT', 'Torrent','줄거리', '공유', '영화', '성인', '야동', '노모', '일본', '유출', '국산', '몰카',
                              '오피', '안마', '유흥', '업소', '키스', '벗방', 'SEX', 'Sex', 'sex', 'Porn', 'porn', 'PORN', '마사지',
                              '토토', '도박', '머니', '스포츠', '베팅', '고액', '배당', '가입', '매충', '지급', '보증', '포커', '경기', '카지노',
                              '환전', '유럽', '중계', '바카라', '먹튀',
                              '토끼', '툰코', '호두코믹스', '포토툰', '늑대닷컴', '펀비']

    title_non_keyword_list = ['불법·유해정보사이트에 대한 차단 안내', '네이버 웹툰', '카카오웹툰 - KAKAO WEBTOON', '레진코믹스 - 솔직한 재미 대폭발', ' 탑툰',
                              '투믹스', '봄툰', '코미코',
                              '미스터블루 - 웹툰, 만화, 소설', '피너툰', '버프툰', 'e북포털 북큐브', '무툰 - 무협,액션 특화 웹툰,만화,소설!',
                              '딜리헙', '포스타입 - POSTYPE', '딜리헙', '애니툰', '온에어 | iMBC', 'SBS 라이브 : 채널 리스트', 'LIVE | 디지털 KBS']

    cnt = 0
    match_result = []

    for title_keyword in title_non_keyword_list:
        if title == title_keyword:
            return cnt
    if '판매용입니다' in title:
        return cnt
    elif '호스팅' in title:
        return cnt


    # if title == '불법·유해정보사이트에 대한 차단 안내':
    #     return cnt
    # elif '판매용입니다' in title:
    #     return cnt
    # elif '호스팅' in title:
    #     return cnt
    # elif title == '네이버 웹툰':
    #     return cnt
    # elif title == '카카오웹툰 - KAKAO WEBTOON':
    #     return cnt
    # elif title == '레진코믹스 - 솔직한 재미 대폭발':
    #     return cnt
    # elif title == ' 탑툰':
    #     return cnt
    # elif title == '투믹스':
    #     return cnt
    # elif title == '봄툰':
    #     return cnt
    # elif title == '코미코':
    #     return cnt
    # elif title == '미스터블루 - 웹툰, 만화, 소설':
    #     return cnt
    # elif title == '피너툰':
    #     return cnt
    # elif title == '버프툰':
    #     return cnt
    # elif title == 'e북포털 북큐브':
    #     return cnt
    # elif title == '무툰 - 무협,액션 특화 웹툰,만화,소설!':
    #     return cnt
    # elif title == '딜리헙':
    #     return cnt
    # elif title == '포스타입 - POSTYPE':
    #     return cnt
    # elif title == '딜리헙':
    #     return cnt
    # elif title == '애니툰':
    #     return cnt
    # elif title == '온에어 | iMBC':
    #     return cnt
    # elif title == 'SBS 라이브 : 채널 리스트':
    #     return cnt
    # elif title == 'LIVE | 디지털 KBS':
    #     return cnt


    for keyword in light_illegal_keywords:
        if keyword in title:
            cnt += 1
            match_result.append(keyword)

        elif keyword not in title:
            if keyword in body:
                cnt += 1
                match_result.append(keyword)

    print(">>> [Verification]...")
    print(">>> [Result] Match Count: [%d]" % cnt, "Match With", match_result)

    return cnt

def run(playwright: Playwright, urls):

    sql_available_urls = []

    unaccessible = 0 #status != 200
    accessible_not_illegal = 0 #status = 200 & 유해사이트 아님
    accessible_illegal = 0 #status = 200 & 유해사이트인경우

    conn = sqlite3.connect("illegals.db")
    for i, url in enumerate(urls):
        try:
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            print("[%d]Checking Response on:" % (i+1), url)
            print(">>> [Requesting]...")
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1440, "height": 2560})

            page = context.new_page()
            response = page.goto(url, timeout=60000)
            if response.status == 200:
                print(">>> [Result] Success! [%d]" %response.status)
                title = page.inner_text("title")
                body = page.inner_text("body")
                result = filtering(title, body) #1 or 0
                #경우의수1) status code가 200이나, 유해사이트가 아닌 경우
                if result < 2:
                    print(">>> [Legal URL]", url, "will be given FALSE")
                    accessible_not_illegal += 1

                    #title, siteavailable False 입력하는 sql코드
                    cur = conn.cursor()

                    sql = "UPDATE " + "illegal_sites" + " SET title = ?, site_available = ? WHERE main_url = ?"
                    # print(sql)

                    cur.execute(sql, (title, False, url))
                    conn.commit()
                # 경우의수2) status code가 200이나, 유해사이트인 경우
                else:
                    page.wait_for_timeout(3000)
                    sql_available_urls.append([url, title])
                    print(">>> [Title]", title)
                    print(">>> [Screnshotting]...")

                    if 'http://' in url:
                        url_go = re.sub(pattern='http://', repl='', string=url)
                        page.screenshot(path=f'./screenshot/{screenshot_time}/{url_go}.png', full_page=False)
                        print('>>> [Screenshot Succeeded]:', url_go)

                    elif 'https://' in url:
                        url_go = re.sub(pattern='https://', repl='', string=url)
                        page.screenshot(path=f'./screenshot/{screenshot_time}/{url_go}.png', full_page=False)
                        print('>>> [Screenshot Succeeded]:', url_go)

                    #report = (reporting 함수)
                    reporting(url, url_go)

                    try:
                        print(">>> [Reporting Succeeded]", url)
                        cur = conn.cursor()
                        sql = "UPDATE " + "illegal_sites" + " SET is_reported = ? WHERE main_url = ?"
                        cur.execute(sql, (True, url))
                        conn.commit()
                    except:
                        print(">>> ")

                    accessible_illegal += 1
                    #title과 site available이 True 입력하는 sql
                    cur = conn.cursor()
                    sql = " UPDATE " + "illegal_sites" + " SET title = ?, site_available = ? WHERE main_url = ?"
                    cur.execute(sql, (title, True, url))
                    conn.commit()

            # 경우의수3) status code가 200이 아니어서 접속 불가한 사이트
            else:
                context.close()
                browser.close()

                # import traceback
                # traceback.print_exc()
                # pass

                unaccessible += 1

                print(">>> [Result] Requesting Failed! [%d]" %response.status)
                print(">>> [Unavailable URL]", url, "will be given 'FALSE'")
                # print("error:", e)

                # site available 0 주는 sql 코드
                cur = conn.cursor()
                sql = " UPDATE " + "illegal_sites" + " SET site_available = ? WHERE main_url = ?"
                cur.execute(sql, ('Status Code - Not 200', url))
                conn.commit()

            context.close()
            browser.close()

        # 경우의수4)request시 code를 뱉지 않고 error를 뱉는 경우
        except Exception as e:

            context.close()
            browser.close()

            import traceback
            traceback.print_exc()
            pass

            unaccessible += 1

            print(">>> [Result] Requesting Failed")
            print(">>> [Unavailable URL]", url, "will be given 'FALSE'")
            # print("error:", e)

            # site available 0 주는 sql 코드
            cur = conn.cursor()
            sql = " UPDATE " + "illegal_sites" + " SET site_available = ? WHERE main_url = ?"
            cur.execute(sql, ('Status Code Error', url))
            conn.commit()

    print("\n[Completed] Please check the overall statistic in below")
    print(">>>[전체: %d]" %len(urls), "[접속불가: %d]" %unaccessible, "[비유해사이트: %d]" %accessible_not_illegal, "[유해사이트: %d]" %accessible_illegal)

    print("\n[List of Illegal Sites]")
    for i in range(len(sql_available_urls)):
        print(">>> [URL]", sql_available_urls[i][0], "[Title]", sql_available_urls[i][1])

def main():

    stdoutOrigin = sys.stdout
    sys.stdout = open('./log/' + screenshot_time + "_log.txt", "w")

    urls = fetch_urls()

    with sync_playwright() as playwright:
        run(playwright, urls)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

if __name__ == '__main__':
    main()