import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import time
from IPython.display import display
import warnings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import pymysql

warnings.filterwarnings(action='ignore')



caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"


options = webdriver.ChromeOptions()

prefs = {'profile.default_content_setting_values': {'cookies'                   : 1, 'images': 2,
                                                        'plugins'                   : 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications'             : 2, 'auto_select_certificate': 2,
                                                        'fullscreen'                : 2,
                                                        'mouselock'                 : 2, 'mixed_script': 2,
                                                        'media_stream'              : 2,
                                                        'media_stream_mic'          : 2, 'media_stream_camera': 2,
                                                        'protocol_handlers'         : 2,
                                                        'ppapi_broker'              : 2, 'automatic_downloads': 2,
                                                        'midi_sysex'                : 2,
                                                        'push_messaging'            : 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop'   : 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement'           : 2,
                                                        'durable_storage'           : 2}}
options.add_experimental_option('prefs', prefs)
#options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--disable-gpu')





def get_video(feature):

    driver = webdriver.Chrome(r"C:\\PythonProjects\\youtubeclooling\\venv\\Scripts\\chromedriver.exe",chrome_options=options)
    driver.set_window_size(700,100)
    driver.get('https://www.youtube.com')





    n = 3
    while n > 0:
        #print('웹페이지를 불러오는 중입니다..' + '..' * n)
        time.sleep(1)



        n -= 1

    src = driver.find_element_by_name("search_query")
    src.send_keys(feature + " 레시피")
    src.send_keys(Keys.RETURN)

    n = 2
    while n > 0:
        #print('검색 결과를 불러오는 중입니다..' + '..' * n)
        time.sleep(1)
        n -= 1

    #print('데이터 수집 중입니다....')

    html = driver.page_source
    soup = BeautifulSoup(html)

    view_list = []
    link_list = []

    for i in range(len(soup.find_all('ytd-video-meta-block', 'style-scope ytd-video-renderer byline-separated'))):


        link = 'https://www.youtube.com/' + soup.find_all('a', {'id': 'video-title'})[i]['href']

        link = link.replace("/watch?v=","embed/")


        soup.find_all('ytd-channel-name', 'long-byline style-scope ytd-video-renderer')[i].text.replace('\n', '').split(
            ' ')[0]
        view = \
        soup.find_all('ytd-video-meta-block', 'style-scope ytd-video-renderer byline-separated')[i].text.split('•')[
            1].split('\n')[3]

        view = view.replace("조회수 ", "")

        if "만회" in view:
            view = view.replace("만회","")
            view = view.replace("만", "")
            iview = float(view)
            iview *= 10000

        elif "천회" in view:
            view = view.replace("천회", "")
            view = view.replace("천", "")
            iview = float(view)
            iview *= 1000
        elif "회" in view:
            view = view.replace("회", "")

            iview = float(view)
        else:
            iview="0"
        iview = int(iview)
        #print("조회수 = " + str(iview) + "   링크 = " + link)

        view_list.append(iview)
        link_list.append(link)

    if len(view_list)==0:
        return
    tmp = max(view_list)
    index = view_list.index(tmp)

    return link_list[index]

    driver.close()





class MysqlController:
    def __init__(self, host, id, pw, db_name):
        try:
            self.conn = pymysql.connect(host=host, user=id, password=pw, db=db_name, charset='utf8')
            self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        except self.conn.DatabaseError as e:
            print(e)
            self.conn.close()


    def insert_youtube(self):

        try:

            sql = 'SELECT * FROM testrecommenddb.foods WHERE (seasonNum is not NULL) or (weatherNum is not NULL)'
            self.curs.execute(sql)
            result = self.curs.fetchall()

            for i in range(len(result)):
                dict = result[i]
                foodName = dict['foodName']
                link = get_video(foodName)

                sql = 'UPDATE foods SET youtubeLink = %s WHERE foodName = %s'
                self.curs.execute(sql, (link, foodName))
                self.conn.commit()
                print("링크삽입 성공! (" + foodName + ")")

            return self.curs.lastrowid


        except self.conn.DatabaseError as e:
            print(e)




mysql_controller = MysqlController('localhost', 'root', 'root', 'testrecommenddb')
mysql_controller.insert_youtube()