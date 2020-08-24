import sqlite3
import json
import pickle
import time
import glob
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class yt_item():
    def __init__(self):
        self.video_id = ''
        self.views = ''
        self.watch_time = ''
        self.subs = ''
        self.impress = ''
        self.video_name=''


def load_cookies():
    '''
        LOAD BROWSER WITH COOKIES
    '''
    driver = webdriver.Firefox(executable_path='drivers/geckodriver')
    with open('cookies/youtube_cookies.pkl', "rb") as pkl:
        cookies = pickle.load(pkl)
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://www.youtube.com/")
    driver.refresh()
    for cookie in cookies:
        # Checks if the instance expiry a float
        if isinstance(cookie.get('expiry'), float):
            # it converts expiry cookie to a int
            cookie['expiry'] = int(cookie['expiry'])
        driver.add_cookie(cookie)
    driver.get("https://www.youtube.com/")
    time.sleep(2)

    '''
        Navigate to the analytics page
    '''

    video_ids = ["pPlJ87tazAg",
                 "wCB_2vnVvZs",
                 "8RFtQB3vVJY",
                 "xcxffv3tTwo",
                 "20gIaAnanlo",
                 "u88qpk-IZ0E",
                 "qxQBXu5dVLY",
                 "2CFCNpevx1c"]
    for video_id in video_ids:
        yt_itm = yt_item()
        driver.get(
            f"https://studio.youtube.com/video/{video_id}/analytics/tab-overview/period-since_publish/explore?entity_type=VIDEO&entity_id={video_id}&time_period=since_publish&explore_type=TABLE_AND_CHART&metric=VIEWS&granularity=DAY&t_metrics[]=VIEWS&t_metrics[]=WATCH_TIME&t_metrics[]=SUBSCRIBERS_NET_CHANGE&t_metrics[]=VIDEO_THUMBNAIL_IMPRESSIONS&t_metrics[]=VIDEO_THUMBNAIL_IMPRESSIONS_VTR&v_metrics[]=VIEWS&v_metrics[]=WATCH_TIME&v_metrics[]=SUBSCRIBERS_NET_CHANGE&v_metrics[]=VIDEO_THUMBNAIL_IMPRESSIONS&v_metrics[]=VIDEO_THUMBNAIL_IMPRESSIONS_VTR&dimension=VIDEO&o_column=VIEWS&o_direction=ANALYTICS_ORDER_DIRECTION_DESC")
        driver.refresh()
        time.sleep(2)

        #/html/body/yta-explore-dialog/ytcp-dialog/paper-dialog/div[2]/yta-explore-app/yta-explore-deep-dive/yta-explore-page/div[2]/div[4]/div/div/div[2]/yta-explore-table/div/yta-explore-table-row/div/div[1]/div/div[2]/yta-title-cell/div/div/span
        video_name = WebDriverWait(driver, 10).until(
            lambda driver:   driver.find_element_by_xpath('/html/body/yta-explore-dialog/ytcp-dialog/paper-dialog/div[2]/yta-explore-app/yta-explore-deep-dive/yta-explore-page/div[2]/div[4]/div/div/div[2]/yta-explore-table/div/yta-explore-table-row/div/div[1]/div/div[2]/yta-title-cell/div/div/span'))
        views = WebDriverWait(driver, 10).until(
            lambda driver:   driver.find_element_by_xpath('/html/body/yta-explore-dialog/ytcp-dialog/paper-dialog/div[2]/yta-explore-app/yta-explore-deep-dive/yta-explore-page/div[2]/div[4]/div/div/div[2]/yta-explore-table/div/yta-explore-table-row/div/div[3]/div[1]/div'))
        watch_time = WebDriverWait(driver, 10).until(
            lambda driver:   driver.find_element_by_xpath('/html/body/yta-explore-dialog/ytcp-dialog/paper-dialog/div[2]/yta-explore-app/yta-explore-deep-dive/yta-explore-page/div[2]/div[4]/div/div/div[2]/yta-explore-table/div/yta-explore-table-row/div/div[4]/div[1]/div'))
        subs = WebDriverWait(driver, 10).until(
            lambda driver:   driver.find_element_by_xpath('/html/body/yta-explore-dialog/ytcp-dialog/paper-dialog/div[2]/yta-explore-app/yta-explore-deep-dive/yta-explore-page/div[2]/div[4]/div/div/div[2]/yta-explore-table/div/yta-explore-table-row/div/div[5]/div[1]/div'))
        impress = WebDriverWait(driver, 10).until(
            lambda driver:   driver.find_element_by_xpath('/html/body/yta-explore-dialog/ytcp-dialog/paper-dialog/div[2]/yta-explore-app/yta-explore-deep-dive/yta-explore-page/div[2]/div[4]/div/div/div[2]/yta-explore-table/div/yta-explore-table-row/div/div[6]/div[1]/div'))

        print(
            f'video id: {video_id}, views: {views.text}, watch time: {watch_time.text}, subscribers {subs.text}, impressions: {impress.text}')

        yt_itm.video_id = video_id
        yt_itm.views = views.text
        yt_itm.watch_time = watch_time.text
        yt_itm.impress = impress.text
        yt_itm.subs = subs.text
        yt_itm.video_name = video_name.text
        pickle.dump(yt_itm, open(
                    f'downloads/{video_id}.pkl', "wb"))

        time.sleep(0.5)
    driver.quit()


def read_Firefox_cookie():
    cookies = []
    conn = sqlite3.connect('db/cookies.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM moz_cookies")
    items = c.fetchall()
    for item in items:
        domain_filed = item[4]
        expiry_field = item[6]
        http_only_field = item[10]
        if http_only_field == 0:
            http_only_field = False
        else:
            http_only_field = True
        name_field = item[2]
        path_field = item[5]
        sameSite_field = 'None'
        secure_field = item[9]
        if secure_field == 0:
            secure_field = False
        else:
            secure_field = True
        value_field = item[3]
        # print(
        #     f'{domain_filed}, {expiry_field}, {http_only_field},{name_field},{path_field},{sameSite_field},{secure_field},{value_field}')

        cookie = {'domain': domain_filed,
                  'expiry': expiry_field,
                  'httpOnly': http_only_field,
                  'name': name_field,
                  'path': path_field,
                  'secure': secure_field,
                  'value': value_field}
        if domain_filed == '.youtube.com':
            print(f'{domain_filed}, {expiry_field}, {http_only_field},{name_field},{path_field},{sameSite_field},{secure_field},{value_field}')
            cookies.append(cookie)
    c.close()
    pickle.dump(cookies, open('cookies/youtube_cookies.pkl', "wb"))
    json.dump(cookies, open('cookies/youtube_cookies.json', "w"))
    print("Cookies have been extracted. Please check the cookies folder.")


def get_csv():
    header = ['video name','video_id', 'views',
              'watch_time', 'impressions', 'subscribers']
    list_lines = []
    # list_lines.append(header)
    counter = 1
    for file in glob.glob("downloads/*.pkl"):
        with open(f"{file}", 'rb') as token:
            item = pickle.load(token)
            #counter += 1
            print(f'{counter}. video id: {item.video_id}, views: {item.views}, watch time: {item.watch_time}, impressions: {item.impress}, subscribers: {item.subs}')

            counter += 1
            list_lines.append(item)
    today = datetime.today().strftime('%Y-%m-%d')

    with open(f'reports/{today}_videos.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        counter = 0
        writer.writeheader()
        for item in list_lines:
                           #['channel_id',            'video_id','         est_mon_playbacks',   'est_revenue',        'views',               'cpm',               'watch_time',         'aver_view_dur',      'aver_perc_viewed',   'impressions',        'subscribers',         'impores_click_thru',         'ad_impres',          'subs_gained',          'subs_lost',          'likes',          'dislikes',          'likes_vs_dislikes',         'shares',          'comments_added']
            writer.writerow({'video name':item.video_name,'video_id': item.video_id, 'views': item.views,
                             'watch_time': item.watch_time, 'impressions': item.impress, 'subscribers': item.subs})
            counter += 1
            print(f'{counter}. {item.video_id} added to csv')


def main():
    load_cookies()
    get_csv()


if __name__ == '__main__':
    main()
