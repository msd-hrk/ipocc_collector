import requests
from bs4 import BeautifulSoup
import re
import datetime
from collector import utils

class ListCollector():
    def __init__(self, data_up, data_down):
        self.data_up = data_up
        self.data_down = data_down
    
    def get_securitiesNo(self):
        tag_data = self.data_up.find(class_='td_code2')
        return tag_data.get_text()
    
    def get_company(self):
        tag_data = self.data_up.select_one('.td_kigyo a')
        return tag_data.get_text()
            
    def get_listingDate(self, securities_no):
        ipo_net_page = 'https://ipokabu.net/ipo/'+ securities_no
        html = requests.get(ipo_net_page)
        soup = BeautifulSoup(html.content, 'html.parser')
        first_sec = soup.select("section")[0]
        txt = first_sec.select(".ta_syosai_sp .f_jojo")[0].get_text()
        arry = txt.split(" ")[0].split("～")[0].split("/")
        return int(datetime.date(int(arry[0]), int(arry[1]), int(utils.del_str(arry[2],"(",")","月","火","水","木","金"))).strftime("%Y%m%d"))

    def get_bookbilding_start(self):
        tag_data = self.data_up.select_one('.ipo_yotei2')
        if tag_data is None:
            tag_data = self.data_up.select_one('.ipo_bosyu2')
        if tag_data is None:
            tag_data = self.data_up.select_one('.td_ipo_syuryo')

        array = str(tag_data.get_text()).split("～")
        start_date = re.search(r'\d{1,2}/\d{1,2}', str(array[0])).group()
        start_date_yyyymmdd = utils.convesion_date_format(start_date)
        return utils.str_to_int(start_date_yyyymmdd)


    def get_bookbilding_end(self):
        tag_data = self.data_up.select_one('.ipo_yotei2')
        if tag_data is None:
            tag_data = self.data_up.select_one('.ipo_bosyu2')
        if tag_data is None:
            tag_data = self.data_up.select_one('.td_ipo_syuryo')

        array = str(tag_data.get_text()).split("～")
        end_date = re.search(r'\d{1,2}/\d{1,2}', str(array[1])).group()
        end_date_yyyymmdd = utils.convesion_date_format(end_date)
        return utils.str_to_int(end_date_yyyymmdd)
            
    def get_grade(self):
        tag_data = self.data_up.select("td")[0].select("span")[0].get_text()
        return tag_data