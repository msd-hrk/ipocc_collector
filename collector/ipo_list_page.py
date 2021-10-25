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
            
    def get_listingDate(self):
        tag_data = self.data_up.select_one('td')
        monthAndDay = re.search(r'\d{1,2}/\d{1,2}', str(tag_data)).group()
        listingDate = utils.convesion_date_format(monthAndDay)
        return utils.str_to_int(listingDate)

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