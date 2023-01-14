# Coding by YES

from censys.search import CensysHosts
import sqlite3
import csv
import os
import time

def get_censys_account_info(API_id, API_pw):
    info = CensysHosts(api_id=API_id, api_secret=API_pw)

    return info

def get_censys_parsing(account_info, title_list):
    api_info = account_info
    flag = len(title_list)

    result = list()
    for f, title in enumerate(title_list):
        # if (f % 299) == 0:
        #     print('API:Search -> 300/5min interval, Waitting for 5min')
        #     time.sleep(300)
        # else:
        for page in api_info.search("services.http.response.html_title: " + title[1], per_page=100):
            for p in page:
                print('[*] ', f, p)
                result.append((title, p))
                time.sleep(0.5)
                if (f % 290) == 0 and f != 0:
                    print('[*] API:Search -> 300/5min interval, Waitting for 5min')
                    time.sleep(300)
    return result

def purify_ip_list(censys_result):
    key_list = ['ip', 'services', 'location', 'autonomous_system']
    location_key = ['country', 'timezone']
    asn_key = ['name', 'bgp_prefix', 'description']

    full_info = list()

    for result in censys_result:
        realip_info = list()
        for r in result[0]:
            realip_info.append(r)
        for t in key_list:
            if t == 'ip':
                realip_info.append(result[1][t])

            elif t == 'services':
                port_list = list()
                for i in result[1][t]:
                    port_list.append((i['port'], i['service_name']))

                realip_info.append(port_list)

            elif t == 'location':
                for key in location_key:
                    realip_info.append(result[1][t][key])

            elif t == 'autonomous_system':
                for key in asn_key:
                    realip_info.append(result[1][t][key])

        full_info.append(realip_info)

    return full_info

def get_keyword(path):
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        # query = r"SELECT main_url, title, ip_address FROM illegal_sites WHERE title != ''"# and site_available == 1" # LIMIT 200, 300"
        query = r"SELECT main_url, title, ip_address, expected_category FROM illegal_sites WHERE title != '' and (expected_category = 'webtoon' or expected_category = 'streaming')"  # and site_available == 1" # LIMIT 200, 300"
        # SELECT * FROM
        # illegal_sites
        # WHERE
        # site_available == 1
        # LIMIT
        # 149, 50

        result = cur.execute(query)

    keyword_list = list()
    tmp_list = list()
    # purify_keyword = ['', 'Cloudflare', '520: Web server', '521: Web', '522: Connection', 'nginx', 'Just a moment', 'not found']
    for re in result:
        re = list(re)

        if re[1] == '' or 'Cloudflare' in re[1] or '521: Web' in re[1] or '522: Connection' in re[1] or 'nginx' in re[1] or 'not found' in re[1]\
                or 'Not Found' in re[1] or 'nginx' in re[1] or '520: Web server' in re[1] or 'Just a moment' in re[1] or '403 Forbidden' in re[1]\
                or 'Loading' in re[1] or 'Account Suspended' in re[1] or 'IIS Windows Server' in re[1] or 'Telegram' in re[1] or 'intro' in re[1] \
                or '업데이트 내역' in re[1] or 'tistory' in re[1] or '网页不存在' in re[1] or '판매용입니다' in re[1] or '点已暂停' in re[1] or '点已暂停' in re[1]\
                or 'BIS' in re[1] or 'Daum' in re[1] or 'TISTORY' in re[1] or 'frontend' in re[1] or 'seo-title' in re[1] or 'MAJOR'in re[1]\
                or 'BETFAIR' in re[1] or '10BET' in re[1] or '日本人妻熟老太' in re[1] or '�' in re[1] or 'Eladó' in re[1] or 'ERROR' in re[1]\
                or 'Access denied' in re[1] or '404' in re[1] or 'youtube' in re[1] or 'something lost' in re[1] or 'blog' in re[1] or 'null' in re[1]\
                or "Google" in re[1] or '403' in re[1] or '아프리카TV' in re[1] or '没有找到站点' in re[1] or 'Website Unavailable' in re[1] or 'Apache' in re[1]\
                or "BIG5" in re[1] or 'Cast' == re[1] or 'NAVER' in re[1] or 'error' in re[1] or 'LUX' in re[1] or 'captcha' in re[1] or 'Not found.' in re[1]\
                or 'Wordpress' in re[1] or 'Blog' in re[1] or 'Acceptable!' in re[1] or '쿠팡' in re[1] or 'youtube' in re[1] or '로그인' in re[1] or '웹하드' in re[1]\
                or '파일노리' in re[1] or 'Stock Music' in re[1] or 'GIGA' in re[1] or "- 사이트 -" in re[1] or 'COD' in re[1] or '차단 안내' in re[1] or 'Amazon' in re[1]\
                or 'ROJADIRECTA' in re[1] or "BitTorrent" in re[1] or "请等待" in re[1] or "스포츠" in re[1] or "휴게소" in re[1] or "YoYo" in re[1] or "마켓" in re[1]:

            continue
        else:
            re[1] = "\"" + re[1] + "\""
            if re[1] in tmp_list:
                continue
            else:
                tmp_list.append(re[1])
                keyword_list.append(re)

    return keyword_list

def export_csv(result):
    real_column = ['main_url', 'title', 'fake_ip', 'real_ip', 'port_list', 'country', 'timezone', 'asn_name', 'bgp_prefix', 'description']
    if os.path.isfile('./result/(2023-01-03)-realip_list.csv'):
        with open('./result/(2023-01-03)-realip_list.csv', 'a', newline='', encoding='utf-8-sig') as f:
            write_csv = csv.writer(f)

            for r in result:
                write_csv.writerow(r)

    else:
        with open('./result/(2023-01-03)-realip_list.csv', 'w', newline='', encoding='utf-8-sig') as f:
            write_csv = csv.writer(f)

            write_csv.writerow(real_column)
            for r in result:
                write_csv.writerow(r)

def main():
    # Suboat(10월 미사용)
    # API_id = 'e440d1d3-4b8c-4ebe-ad5b-eb5b1a32e3f5'
    # API_pw = 'kJO3FKovTGmNCYnyv2w0v5IFUgPoPkZK'

    # Official Copyright
    API_id = 'f7a3a296-89ea-49f2-811b-b59df6d1bafb'
    API_pw = 'vwcyP272IkReUSdyw7SMX1uHL8cc89wl'

    # HoDDI
    # API_id = '66017627-01e9-4db0-a052-a4185f10a13d'
    # API_pw = 'g0aeCknVAFJr1lsoXoYbymWLpFy10V5t'

    # Center Jeong
    # API_id = '1593fc73-e337-4208-aa91-22534088c769'
    # API_pw = 'uarwRIr6bNcwz0riA7V9DVJZ9IN47Qbh'
    #
    # # mingming
    # API_id = '8d4d0f7c-3426-4f15-b137-c94536a50a7a'
    # API_pw = 'trythKrmSRRprbqObP8XKaQ8KbT7mRUc'
    #
    # # taylor
    # API_id = '2b5ddd21-98c8-437a-bb9e-a6c5f57ecec1'
    # API_pw = 'qMGGNItiUZi5WW1GBz6X6EKSVk6ai9Q5'
    #
    # # lumme
    # API_id = '82d0602c-e96d-4ba6-9415-8eef74ef4011'
    # API_pw = 'sxiwYZinlIpm1l6KbV0GtUGFmxBdrAwT'
    #
    # piki
    # API_id = 'ad9a38e3-9743-48c5-a7ec-9c387ee98cad'
    # API_pw = 'ctQjPU2w485zdp4Bn2nMLtfWxLKlpE5s'


    # api:search 1.0 actions/second (300.0 per 5 minute interval)
    # Operation Interval: 5min, 300
    title_list = get_keyword("./db/0102_illegals.db")
    print('[*] Site Number: ' + str(len(title_list)))
    print(title_list)
    api_info = get_censys_account_info(API_id, API_pw)
    realip_list = get_censys_parsing(api_info, title_list)
    purify_realip = purify_ip_list(realip_list)
    export_csv(purify_realip)
    # print(purify_realip)

if __name__ == '__main__':
    main()